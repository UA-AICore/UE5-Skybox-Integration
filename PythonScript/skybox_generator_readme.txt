
Skybox Generator for Unreal Engine 5

1. Set Environment Variables:
   - Add the following lines to your ~/.bashrc or ~/.zshrc:
     export OPENAI_API_KEY="your_openai_api_key"
     export BLOCKADE_LABS_API_KEY="your_blockade_labs_api_key"
   - Source the file:
     source ~/.bashrc

2. Install Python Dependencies:
   - Unreal Engine uses an embedded Python environment. Install the required libraries:
     /Users/Shared/Epic\ Games/UE_5.4/Engine/Binaries/ThirdParty/Python3/Mac/bin/python3 -m pip install openai requests

3. Update the Base Prompt:
   - Open the script in Visual Studio Code:
     open -a "Visual Studio Code" "/Users/Shared/Epic Games/UE_5.4/Engine/Binaries/Mac/skybox_script_ue5.py"
   - Modify the 'base_prompt' variable in the script to your desired skybox description.

4. Run the Script in Unreal Engine:
   - Enable the Python plugin in Unreal Engine: Edit > Plugins > Scripting > Python.
   - Open the Python terminal in Unreal Engine: Window > Developer Tools > Python.
   - Run the script in the Python terminal:
     exec(open("/Users/Shared/Epic Games/UE_5.4/Engine/Binaries/Mac/skybox_script_ue5.py").read())

5. Troubleshooting:
   - Ensure environment variables are correctly set and sourced.
   - Check prompt length (max 600 characters).
   - Install any missing Python modules in Unreal's Python environment.

Enjoy creating amazing skyboxes!
