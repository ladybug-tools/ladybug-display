# coding=utf-8
# import the core ladybug modules
from ladybug.compass import Compass
from ladybug.sunpath import Sunpath
from ladybug.windrose import WindRose
from ladybug.windprofile import WindProfile
from ladybug.hourlyplot import HourlyPlot
from ladybug.monthlychart import MonthlyChart
from ladybug.psychchart import PsychrometricChart

# import the extension functions
from .extension.compass import compass_to_vis_set
from .extension.sunpath import sunpath_to_vis_set
from .extension.windrose import wind_rose_to_vis_set
from .extension.windprofile import wind_profile_to_vis_set
from .extension.hourlyplot import hourly_plot_to_vis_set
from .extension.monthlychart import monthly_chart_to_vis_set
from .extension.psychchart import psychrometric_chart_to_vis_set

# inject the methods onto the classes
Compass.to_vis_set = compass_to_vis_set
Sunpath.to_vis_set = sunpath_to_vis_set
WindRose.to_vis_set = wind_rose_to_vis_set
WindProfile.to_vis_set = wind_profile_to_vis_set
HourlyPlot.to_vis_set = hourly_plot_to_vis_set
MonthlyChart.to_vis_set = monthly_chart_to_vis_set
PsychrometricChart.to_vis_set = psychrometric_chart_to_vis_set

# try to extend ladybug-radiance
try:
    # import the ladybug-radiance modules
    from ladybug_radiance.visualize.skydome import SkyDome
    from ladybug_radiance.visualize.radrose import RadiationRose
    from ladybug_radiance.visualize.raddome import RadiationDome
    from ladybug_radiance.study.directsun import DirectSunStudy
    from ladybug_radiance.study.radiation import RadiationStudy

    # import the extension functions
    from .extension.skydome import sky_dome_to_vis_set
    from .extension.radrose import radiation_rose_to_vis_set
    from .extension.raddome import radiation_dome_to_vis_set
    from .extension.study.directsun import direct_sun_study_to_vis_set
    from .extension.study.radiation import radiation_study_to_vis_set

    # inject the methods onto the classes
    SkyDome.to_vis_set = sky_dome_to_vis_set
    RadiationRose.to_vis_set = radiation_rose_to_vis_set
    RadiationDome.to_vis_set = radiation_dome_to_vis_set
    DirectSunStudy.to_vis_set = direct_sun_study_to_vis_set
    RadiationStudy.to_vis_set = radiation_study_to_vis_set
except ImportError:
    pass  # ladybug-radiance is not installed
