from hnlp.config import ARCH

if ARCH == "tf":
    from hnlp.model.model_tf import cls_model, cosine_model
else:
    raise NotImplementedError
