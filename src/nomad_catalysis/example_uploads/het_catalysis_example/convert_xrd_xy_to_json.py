import os
import json
from datetime import datetime

def parse_file(file_name):
    data = {}
    intensity = []
    two_theta = []

    with open(file_name, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if line.startswith(';'):
            continue
        if line.strip() == '':
            continue
        
        # Check if the line contains data for intensity and two_theta
        values = line.strip().split()
        if len(values) == 2:
            two_theta.append(float(values[0]))
            intensity.append(float(values[1]))
        else:
            key, value = line.strip().split(' = ')
            key = key.strip('_').lower()
            data[key] = value
        data['datafile'] = file_name
        split_filename = file_name.split('_')
        data['datemeasured'] = split_filename[0].split('R')[0]
        data['sample'] = 'FHI_S'+ str(split_filename[1])

    return data, intensity, two_theta

def generate_json(data, intensity, two_theta):
    json_data = {
        "data": {
            "m_def": "nomad_measurements.xrd.schema.ELNXRayDiffraction",
            "diffraction_method_name": 'Powder X-Ray Diffraction (PXRD)',
            "location": "FHI/AC department",
            "datetime": data["datemeasured"],
            "data_file": data["datafile"],
            "samples": [{
                "lab_id": data["sample"]
            }],
            "xrd_settings": {
                "source":{
                    "xray_tube_material": 'Cu',
                    "kalpha_one": 1.5406,
                    "kalpha_two": 1.54439,
                    "ratio_kalphatwo_kalphaone": 0.5,
                    "kbeta": 1.39222
                },
            },
            "results": [{
                "m_def": "nomad_measurements.xrd.schema.XRDResult1D",
                "intensity": intensity,
                "two_theta": two_theta,
                "source_peak_wavelength": 1.5406
            }]
        }
    }
    return json_data

def main():
    for file_name in os.listdir('.'):
        if file_name.endswith('.xyd'):
            data, intensity, two_theta = parse_file(file_name)
            data["datemeasured"] = datetime.strptime(data["datemeasured"], "%y%m%d")
            data["datafile"] = file_name
            json_data = generate_json(data, intensity, two_theta)
            output_file_name = file_name.split('.')[0] + '.archive.json'
            with open(output_file_name, 'w') as json_file:
                json.dump(json_data, json_file, indent=4, default=str)

if __name__ == "__main__":
    main()