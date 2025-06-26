# I just want to know what number to use
- Run `uv venv` 
- Run `uv pip install -r pyproject.toml`
- Run `python ./EDID-Solver.py`
- Enter your monitor's rated peak brightness in nits.
- Pick one and set your Max Luminance in the HDR metadata section in your CRU

# I want to do my own math or development, thank you
- Run `uv venv` and `uv pip install -r pyproject.toml --all-extras`

## What is this?
RTX HDR is fantastic for HDR game content, but not so great for users. It assumes your monitor has its peak brightness encoded in its EDID according to some math that I have not seen used outside of the NVIDIA App. This is used even if your monitor has a fancy color calibration profile. I did a very simple reverse engineering of the curve they use to calculate your monitor's peak brightness in nits from the little data they expose in the app. It's not a perfect remapping, but this lets you set a number in CRU, restart your graphics driver, and then never think about it again. This will give you VASTLY better results than what is usually set by default in monitors...
