"""
run_validate.py
run functions defined in validate.py
"""
from validate import generate_comparison_files, validate_files

def main():
    """
    main entrypoint for running the acoustic-features validation scripts
    """
    sample_filepath = '../sample_audio/first_ten_Sample_HV_Clip.wav'
    generate_comparison_files(sample_filepath)
    md_out = 'my-env-validate.md'
    with open(md_out, 'w') as outfile:
        outfile.write('# My Environment, run_validate.py\n')
        outfile.write("```sh\n")
    validate_files(sample_filepath, 'python3-13-1')
    validate_files(sample_filepath, 'python3-9-6')
    validate_files(sample_filepath, 'debian_docker_python3-9-6')
    with open(md_out, 'a') as outfile:
        outfile.write("\n```")

if __name__ == '__main__':
    main()
