import sys, os, shutil


def main():
    proj_dir = "{{ cookiecutter.project_name }}".lower()
    os.chdir(proj_dir)
    print(os.getcwd())
if __name__ == '__main__':
      sys.exit(main())