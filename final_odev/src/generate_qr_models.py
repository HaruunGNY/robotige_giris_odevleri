#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import urllib.request
import cv2

# Configuration
MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models"))
GOREV_NOKTALARI = {
    "qr_information_desk": {
        "data": "LOCATION=INFORMATION_DESK",
        "material_name": "QR_InformationDesk/Material",
        "texture_filename": "qr_info.png"
    },
    "qr_science_section": {
        "data": "LOCATION=SCIENCE_SECTION",
        "material_name": "QR_ScienceSection/Material",
        "texture_filename": "qr_science.png"
    },
    "qr_novel_section": {
        "data": "LOCATION=NOVEL_SECTION",
        "material_name": "QR_NovelSection/Material",
        "texture_filename": "qr_novel.png"
    },
    "qr_checkout_area": {
        "data": "LOCATION=CHECKOUT_AREA",
        "material_name": "QR_CheckoutArea/Material",
        "texture_filename": "qr_checkout.png"
    }
}

def create_directory_structure(model_name):
    model_path = os.path.join(MODELS_DIR, model_name)
    textures_dir = os.path.join(model_path, "materials", "textures")
    scripts_dir = os.path.join(model_path, "materials", "scripts")
    
    os.makedirs(textures_dir, exist_ok=True)
    os.makedirs(scripts_dir, exist_ok=True)
    return model_path, textures_dir, scripts_dir

def download_qr_code(data, output_path):
    # Safe URL encoding
    safe_data = urllib.parse.quote(data)
    url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={safe_data}"
    print(f"Downloading QR for '{data}'...")
    try:
        urllib.request.urlretrieve(url, output_path)
        print("Success.")
    except Exception as e:
        print(f"Error downloading QR code: {e}")

def create_model_config(model_path, model_name):
    config_content = f"""<?xml version="1.0"?>
<model>
  <name>{model_name}</name>
  <version>1.0</version>
  <sdf version="1.6">model.sdf</sdf>
  <author>
    <name>Harun</name>
    <email>harun@todo.todo</email>
  </author>
  <description>QR Code Model for {model_name}</description>
</model>
"""
    with open(os.path.join(model_path, "model.config"), "w") as f:
        f.write(config_content)

def create_material_script(scripts_dir, material_name, texture_filename):
    material_content = f"""material {material_name}
{{
  technique
  {{
    pass
    {{
      lighting off
      texture_unit
      {{
        texture {texture_filename}
      }}
    }}
  }}
}}
"""
    # Material script filename matches model name but in scripts dir
    script_path = os.path.join(scripts_dir, "qr_code.material")
    with open(script_path, "w") as f:
        f.write(material_content)

def create_model_sdf(model_path, model_name, material_name):
    # Visual has the material applied, thickness = 0.001, width = 0.3, height = 0.3.
    # Center is at z = 0.15 so it stands on the ground.
    # Front-facing (applied on front face)
    sdf_content = f"""<?xml version="1.0" ?>
<sdf version="1.6">
  <model name="{model_name}">
    <static>true</static>
    <link name="link">
      <pose>0 0 0.15 0 0 0</pose>
      <collision name="collision">
        <geometry>
          <box>
            <size>0.02 0.3 0.3</size>
          </box>
        </geometry>
      </collision>
      <visual name="visual">
        <pose>0.011 0 0 0 0 0</pose>
        <geometry>
          <box>
            <size>0.001 0.3 0.3</size>
          </box>
        </geometry>
        <material>
          <script>
            <uri>model://{model_name}/materials/scripts</uri>
            <uri>model://{model_name}/materials/textures</uri>
            <name>{material_name}</name>
          </script>
        </material>
      </visual>
    </link>
  </model>
</sdf>
"""
    with open(os.path.join(model_path, "model.sdf"), "w") as f:
        f.write(sdf_content)

def main():
    print(f"Generating QR models in {MODELS_DIR}...")
    for model_name, info in GOREV_NOKTALARI.items():
        print(f"\n--- Processing {model_name} ---")
        model_path, textures_dir, scripts_dir = create_directory_structure(model_name)
        
        # Download QR code PNG with unique name
        texture_filename = info["texture_filename"]
        img_path = os.path.join(textures_dir, texture_filename)
        download_qr_code(info["data"], img_path)
        
        # Convert 1-bit colormap PNG to standard 24-bit BGR PNG to avoid Ogre loading bugs
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        if img is not None:
            cv2.imwrite(img_path, img)
            print("Successfully converted PNG to standard 24-bit BGR format.")
        else:
            print("Warning: Failed to read downloaded PNG using OpenCV!")
        
        # Create config and sdf files
        create_model_config(model_path, model_name)
        create_material_script(scripts_dir, info["material_name"], texture_filename)
        create_model_sdf(model_path, model_name, info["material_name"])
        
    print("\nAll QR models generated successfully!")

if __name__ == "__main__":
    main()
