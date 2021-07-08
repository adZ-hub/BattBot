import unittest
import pybamm
import multiprocessing
from bot.plotting.random_plot_generator import random_plot_generator
import os


class TestRandomPlotGenerator(unittest.TestCase):

    def tearDown(self):
        if os.path.exists("plot.png"):
            os.remove("plot.png")
        if os.path.exists("plot.gif"):
            os.remove("plot.gif")

    def test_random_plot_generator(self):

        key_list = [
            "particle mechanics",
            "lithium plating",
            "SEI",
            "lithium plating porosity change"
        ]

        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        while True:
            p = multiprocessing.Process(
                target=random_plot_generator, args=(
                    return_dict,
                    {
                        "testing": True,
                        "choice": "degradation comparisons",
                        "chemistry": pybamm.parameter_sets.Chen2020,
                        "provided_degradation": True
                    }
                )
            )
            p.start()
            p.join(600)

            if p.is_alive():
                print(
                    "Simulation is taking too long, "
                    + "KILLING IT and starting a NEW ONE."
                )
                curr_dir = os.getcwd()
                for file in os.listdir(curr_dir):
                    if file.startswith("plot"):
                        os.remove(file)
                p.kill()
                p.join()
            else:
                break

        self.assertIsInstance(return_dict["model"], pybamm.BaseBatteryModel)
        self.assertIsNotNone(return_dict["model"].options)
        self.assertIsInstance(return_dict["model"].options, dict)
        self.assertTrue(
            key in key_list for key in return_dict["model"].options.keys()
        )
        self.assertEqual("lithium_ion", return_dict["chemistry"]["chemistry"])
        self.assertIsNotNone(return_dict["cycle"])
        self.assertIsNotNone(return_dict["number"])
        self.assertTrue(return_dict["is_experiment"])
        self.assertTrue(return_dict["is_summary_variable"])
        self.assertEqual(return_dict["degradation_mode"], "SEI")
        self.assertTrue(
            return_dict["degradation_value"] == "ec reaction limited"
            or return_dict["degradation_value"] == "reaction limited"
            or return_dict["degradation_value"] == "solvent-diffusion limited"
            or return_dict["degradation_value"] == "electron-migration limited"
            or return_dict["degradation_value"] ==
            "interstitial-diffusion limited"
        )
        self.assertIsInstance(return_dict["param_to_vary"], str)
        pybamm.Experiment(return_dict["cycle"] * return_dict["number"])

        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        while True:
            p = multiprocessing.Process(
                target=random_plot_generator, args=(
                    return_dict,
                    {
                        "testing": True,
                        "choice": "degradation comparisons",
                        "chemistry": pybamm.parameter_sets.Ai2020,
                        "provided_degradation": True
                    }
                )
            )
            p.start()
            p.join(600)

            if p.is_alive():
                print(
                    "Simulation is taking too long, "
                    + "KILLING IT and starting a NEW ONE."
                )
                curr_dir = os.getcwd()
                for file in os.listdir(curr_dir):
                    if file.startswith("plot"):
                        os.remove(file)
                p.kill()
                p.join()
            else:
                break

        self.assertIsInstance(return_dict["model"], pybamm.BaseBatteryModel)
        self.assertIsNotNone(return_dict["model"].options)
        self.assertIsInstance(return_dict["model"].options, dict)
        self.assertTrue(
            key in key_list for key in return_dict["model"].options.keys()
        )
        self.assertEqual("lithium_ion", return_dict["chemistry"]["chemistry"])
        self.assertIsNotNone(return_dict["cycle"])
        self.assertIsNotNone(return_dict["number"])
        self.assertTrue(return_dict["is_experiment"])
        self.assertTrue(return_dict["is_summary_variable"])
        self.assertEqual(
            return_dict["degradation_mode"], "particle mechanics"
        )
        self.assertTrue(
            return_dict["degradation_value"] == "swelling and cracking"
        )
        self.assertIsInstance(return_dict["param_to_vary"], str)

        pybamm.Experiment(return_dict["cycle"] * return_dict["number"])

        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        while True:
            p = multiprocessing.Process(
                target=random_plot_generator, args=(
                    return_dict,
                    {
                        "testing": True,
                        "choice": "non-degradation comparisons",
                        "chemistry": None,
                        "provided_degradation": True
                    }
                )
            )
            p.start()
            p.join(1200)

            if p.is_alive():
                print(
                    "Simulation is taking too long, "
                    + "KILLING IT and starting a NEW ONE."
                )
                curr_dir = os.getcwd()
                for file in os.listdir(curr_dir):
                    if file.startswith("plot"):
                        os.remove(file)
                p.kill()
                p.join()
            else:
                break

        for model in return_dict["model"].values():
            self.assertIsInstance(model, pybamm.BaseBatteryModel)
            self.assertIsNotNone(model.options)
            self.assertIsInstance(model.options, dict)
            self.assertTrue(key in key_list for key in model.options.keys())
        self.assertEqual("lithium_ion", return_dict["chemistry"]["chemistry"])
        self.assertIsInstance(return_dict["is_experiment"], bool)
        self.assertIsInstance(return_dict["is_summary_variable"], bool)


if __name__ == "__main__":
    unittest.main()
