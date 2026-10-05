import os
import argparse
import zipfile


def zip_dir(dirpath: str, out_path: str):
    zip = zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED)
    for python_file in ['rotation.py', 'robot_model.py']:
        zip.write(python_file, python_file)
    zip.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--id", type=str, default="2000010000", help="学号，如2000010000"
    )
    parser.add_argument(
        "--name", type=str, default="ZhangSan", help="姓名拼音，如ZhangSan"
    )
    args = parser.parse_args()

    zip_name = f"{args.id}_{args.name}.zip"
    current_file_directory_path = os.path.dirname(os.path.abspath(__file__))
    input_path = current_file_directory_path
    output_path = os.path.join(current_file_directory_path, zip_name)

    zip_dir(input_path, output_path)