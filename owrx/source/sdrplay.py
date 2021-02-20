from owrx.source.soapy import SoapyConnectorSource, SoapyConnectorDeviceDescription
from owrx.form import Input, CheckboxInput, DropdownInput, DropdownEnum
from owrx.form.device import BiasTeeInput
from owrx.form.converter import OptionalConverter, EnumConverter
from typing import List


class SdrplaySource(SoapyConnectorSource):
    def getSoapySettingsMappings(self):
        mappings = super().getSoapySettingsMappings()
        mappings.update(
            {
                "bias_tee": "biasT_ctrl",
                "rf_notch": "rfnotch_ctrl",
                "dab_notch": "dabnotch_ctrl",
                "if_mode": "if_mode",
                "external_reference": "extref_ctrl",
            }
        )
        return mappings

    def getDriver(self):
        return "sdrplay"


class IfModeOptions(DropdownEnum):
    IFMODE_ZERO_IF = "Zero-IF"
    IFMODE_450 = "450kHz"
    IFMODE_1620 = "1620kHz"
    IFMODE_2048 = "2048kHz"

    def __str__(self):
        return self.value


class SdrplayDeviceDescription(SoapyConnectorDeviceDescription):
    def getGainStages(self):
        return ["RFGR", "IFGR"]

    def getInputs(self) -> List[Input]:
        return self.mergeInputs(
            super().getInputs(),
            [
                BiasTeeInput(),
                CheckboxInput(
                    "rf_notch",
                    "",
                    checkboxText="Enable RF notch filter",
                    converter=OptionalConverter(defaultFormValue=True),
                ),
                CheckboxInput(
                    "dab_notch",
                    "",
                    checkboxText="Enable DAB notch filter",
                    converter=OptionalConverter(defaultFormValue=True),
                ),
                DropdownInput(
                    "if_mode",
                    "IF Mode",
                    IfModeOptions,
                    converter=OptionalConverter(
                        EnumConverter(IfModeOptions), defaultFormValue=IfModeOptions.IFMODE_ZERO_IF.name
                    ),
                ),
            ],
        )
