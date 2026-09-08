import glob
import os
import subprocess
from distutils.cmd import Command

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py


class TrainModel(Command):
    description = "Training the model before building the package"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        PYTHONPATH = os.environ.get("PYTHONPATH", "")
        # Training iterates a Python set, so the resulting model depends on the
        # interpreter's hash seed. Pin it, or every run produces a different model.
        os.environ.setdefault("PYTHONHASHSEED", "1")

        # Remove any existing models first. Otherwise parserator renames each one to a
        # timestamped backup, littering the package directory.
        for existing_model in glob.glob("probablepeople/*.crfsuite"):
            os.remove(existing_model)

        subprocess.run(
            [
                "parserator",
                "train",
                "name_data/labeled/person_labeled.xml,name_data/labeled/company_labeled.xml",
                "probablepeople",
                "--modelfile=generic",
            ],
            env=dict(os.environ, PYTHONPATH=f".{os.pathsep}{PYTHONPATH}"),
        )
        subprocess.run(
            [
                "parserator",
                "train",
                "name_data/labeled/person_labeled.xml",
                "probablepeople",
                "--modelfile=person",
            ],
            env=dict(os.environ, PYTHONPATH=f".{os.pathsep}{PYTHONPATH}"),
        )
        subprocess.run(
            [
                "parserator",
                "train",
                "name_data/labeled/company_labeled.xml",
                "probablepeople",
                "--modelfile=company",
            ],
            env=dict(os.environ, PYTHONPATH=f".{os.pathsep}{PYTHONPATH}"),
        )


MODEL_FILES = [
    "probablepeople/company_learned_settings.crfsuite",
    "probablepeople/generic_learned_settings.crfsuite",
    "probablepeople/person_learned_settings.crfsuite",
]


class build_py(_build_py):
    def run(self):
        # Train only when the models are missing. Distributions that ship prebuilt
        # models skip this; run ./train_models.sh to regenerate them deliberately.
        if all(os.path.exists(model_file) for model_file in MODEL_FILES):
            print("Trained models already present, skipping training.")
        else:
            self.run_command("train_model")
        super().run()


# Standard setup configuration
setup(
    cmdclass={
        "build_py": build_py,  # Override build_py
        "train_model": TrainModel,  # Register custom command
    },
)
