import logging

def get_logger(name, log_file=None, level=logging.INFO):
    """
    Retourne un logger formaté prêt à l’emploi (singleton par nom).
    Permet de logger vers la console OU un fichier (ou les deux si besoin), avec niveau paramétrable.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        if log_file:
            fh = logging.FileHandler(log_file, encoding="utf-8")
            fh.setFormatter(formatter)
            logger.addHandler(fh)
        else:
            sh = logging.StreamHandler()
            sh.setFormatter(formatter)
            logger.addHandler(sh)
    return logger
