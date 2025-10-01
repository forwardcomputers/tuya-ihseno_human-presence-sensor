
import asyncio
from typing import Any

from zigpy.quirks.v2 import EntityPlatform, EntityType
from zigpy.quirks.v2.homeassistant import LIGHT_LUX, UnitOfLength, UnitOfTime
from zigpy.quirks.v2.homeassistant.binary_sensor import BinarySensorDeviceClass
from zigpy.quirks.v2.homeassistant.sensor import SensorDeviceClass, SensorStateClass
import zigpy.types as t
from zigpy.zcl.clusters.measurement import OccupancySensing
from zigpy.zcl.clusters.security import IasZone

from zhaquirks.tuya import TuyaLocalCluster
from zhaquirks.tuya.builder import TuyaQuirkBuilder


class TuyaOccupancySensing(OccupancySensing, TuyaLocalCluster):
    """Tuya local OccupancySensing cluster."""


class TuyaMotionSensorMode(t.enum8):
    """Tuya motion sensor mode enum."""

    On = 0x00
    Off = 0x01
    Occupied = 0x02
    Unoccupied = 0x03


class TuyaMotionPresenceSensitivity(t.enum8):
    """Tuya motion presence sensitivity enum."""

    Low = 0x00
    Medium = 0x01
    High = 0x02


class TuyaMotionFadeTime(t.enum8):
    """Tuya motion fade time enum."""

    _15_seconds = 0x00
    _30_seconds = 0x01
    _60_seconds = 0x02


(
    TuyaQuirkBuilder("_TZE284_debczeci", "TS0601")
    .tuya_dp(
        dp_id=1,
        ep_attribute=TuyaOccupancySensing.ep_attribute,
        attribute_name=OccupancySensing.AttributeDefs.occupancy.name,
        converter=lambda x: x == 0,
    )
    .adds(TuyaOccupancySensing)
    .tuya_battery(dp_id=4)
    .tuya_enum(
        dp_id=9,
        attribute_name="presence_sensitivity",
        enum_class=TuyaMotionPresenceSensitivity,
        translation_key="presence_sensitivity",
        fallback_name="Presence sensitivity",
    )
    .tuya_enum(
        dp_id=10,
        attribute_name="fading_time",
        enum_class=TuyaMotionFadeTime,
        translation_key="fading_time",
        fallback_name="Fading time",
    )
    .skip_configuration()
    .add_to_registry()
)

