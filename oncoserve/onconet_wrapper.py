import logging
import torch
import torch.autograd as autograd
import oncoserve.logger
import onconet.utils.parsing as parsing
from  onconet.transformers.basic import ComposeTrans
import  onconet.transformers.factory as transformer_factory
import oncoserve.aggregators.factory as aggregator_factory
import pdb

INIT_MESSAGE = "OncoNet- Initializing OncoNet Wrapper..."
TRANSF_MESSAGE = "OncoNet- Transfomers succesfully composed"
MODEL_MESSAGE = "OncoNet- Model successfully loaded from : {}"
AGGREGATOR_MESSAGE = "OncoNet- Aggregator [{}] succesfully loaded"
IMG_CLASSIF_MESSAGE = "OncoNet- Image classification produced {}"
EXAM_CLASSIF_MESSAGE = "OncoNet- Exam classification complete!"


class OncoNetWrapper(object):
    def __init__(self, args, aggregator_name, logger):
        logger.info(INIT_MESSAGE)
        self.args = args
        args.cuda = args.cuda and torch.cuda.is_available()
        args.test_image_transformers = parsing.parse_transformers(args.test_image_transformers)
        args.test_tensor_transformers = parsing.parse_transformers(args.test_tensor_transformers)
        test_transformers = transformer_factory.get_transformers(
            args.test_image_transformers, args.test_tensor_transformers, args)


        self.transformer = ComposeTrans(test_transformers)
        logger.info(TRANSF_MESSAGE)
        self.model = torch.load(args.snapshot)
        logger.info(MODEL_MESSAGE.format(args.snapshot))
        self.aggregator = aggregator_factory.get_exam_aggregator(aggregator_name)

        self.logger = logger


    def process_image(self, image):
        ## Apply transformers
        x = self.transformer(image, self.args.additional)
        x = x.unsqueeze(0)
        x = autograd.Variable(x)
        if self.args.cuda:
            x = x.cuda()
        pred_y = self.model(x)
        #Find max pred
        pred_y = self.args.label_map[ pred_y.cpu().data.numpy().argmax() ]
        self.logger.info(IMG_CLASSIF_MESSAGE.format(pred_y))
        return pred_y

    def process_exam(self, images):
        preds = []
        for im in images:
            preds.append(self.process_image(im))
        y = self.aggregator(preds)
        self.logger.info(EXAM_CLASSIF_MESSAGE)
        return y
