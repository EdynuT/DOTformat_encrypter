import os
import subprocess
import sys

def create_virtualenv(venv_path):
    subprocess.check_call([sys.executable, '-m', 'venv', venv_path])
    print(f"Virtual environment created at {venv_path}")

def install_dependencies(venv_path):
    pip_path = os.path.join(venv_path, 'Scripts', 'pip') if os.name == 'nt' else os.path.join(venv_path, 'bin', 'pip')
    requirements_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'requirements.txt')
    subprocess.check_call([pip_path, 'install', '-r', requirements_path])
    print("Dependencies installed")

def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    venv_path = os.path.join(project_root, 'venv')

    if not os.path.exists(venv_path):
        create_virtualenv(venv_path)
    install_dependencies(venv_path)

if __name__ == '__main__':
    main()