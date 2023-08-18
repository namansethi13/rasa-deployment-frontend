import streamlit as st
import zipfile
import shutil
import os
import subprocess
import platform
import requests
# create bash file , default requirements.txt
def run_command_with_output(command,name):
    cw = os.path.join(".", "extracted_folder", name)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True, cwd=cw)
    container = st.empty()
    while True:
        try:
            output = process.stdout.readline()
            if output:
                # print(output.strip())
                with open("output.log", "a") as log_file:
                    log_file.write(output)
                container.text(output)
        except:
            continue


def deploy(folder):
    shutil.copytree("./docker_files", f"./extracted_folder/{folder}/",dirs_exist_ok=True)
    shutil.copytree("./bash_folder", f"./extracted_folder/{folder}/",dirs_exist_ok=True)
    #check if requirements.txt exists in actions folder
    if not os.path.exists(f"./extracted_folder/{folder}/actions/requirements.txt"):
        #modify Dockerfile.rasa-os and remove line 5 from it
       with open(f"./extracted_folder/{folder}/actions/requirements.txt", "w") as file:
         file.write("")
    # run command docker compose up
    command_to_run = "deploy.bat" if platform.system() == "Windows" else "./deploy.sh"
    run_command_with_output(command_to_run,folder)
   

    

def main():
    st.title("One click rasa deploy!")
    with st.expander("See requirements"):

        st.markdown("# Rasa Folder Structure")
        st.write("The Rasa folder should contain the following files:")
        st.markdown(
            "- `actions/actions.py`\n"
            "- `data/nlu.yml`\n"
            "- `data/rules.yml`\n"
            "- `data/stories.yml`\n"
            "- `config.yml`\n"
            "- `domain.yml`\n"
            "- `endpoints.yml`"
        )
        st.write("*Create a requirements.txt file if you are using libraries in the rasa actions*")
    rasa_file = st.file_uploader(label="Upload the rasa folder in zip format without the models and .rasa folder", type=['zip'])

    dirs = os.listdir("./extracted_folder")
    if len(dirs) != 0:
        st.sidebar.text("Following folders were found:")
        with st.spinner("Loading"):
            del_btn = st.sidebar.button("Delete")
            existing_files = {}
            for d in dirs:
                s = st.sidebar.checkbox(f"{d}")
                existing_files[d] = s
        if del_btn:
            files_deleted_dict = []
            for f in existing_files:
                if  existing_files[f] == True:
                    files_deleted_dict.append(f)
            for d in files_deleted_dict:
                try:
                    shutil.rmtree(f"./extracted_folder/{d}")
                except:
                    st.info(f"Cannot delete {d}")
            st.experimental_rerun()
        

    if rasa_file is not None:
        deploy_btn = st.button("Deploy!")

        
        if deploy_btn:
            st.success("Deploying!")
            
            if not os.path.exists("./extracted_folder"):
                os.makedirs("extracted_folder")
            
            with zipfile.ZipFile(rasa_file, 'r') as zip_ref:
                zip_ref.extractall("./extracted_folder")
                st.success("Uploaded!")
                
                name = rasa_file.name.split(".")[0]
                # st.info(name)
                
                required_files = [
                    f"actions/actions.py",
                    f"data/nlu.yml",
                    f"data/rules.yml",
                    f"data/stories.yml",
                    f"config.yml",
                    f"domain.yml",
                    f"endpoints.yml"
                ]
                
                missing_files = []
                for file_path in required_files:
                    full_path = os.path.join("extracted_folder", name, file_path)
                    if not os.path.exists(full_path):
                        missing_files.append(file_path)
                        st.info(full_path)
                
                if missing_files:
                    st.error("Invalid rasa folder. Missing files:")
                    for missing_file in missing_files:
                        st.write("- " + missing_file)
            
                else:
                    if not os.path.exists(f"./extracted_folder/{name}/actions/requirements.txt"):
                        st.warning("requirements.txt file not found in the actions folder, create a requirements file if you are using any library other than rasa_sdk")
                    st.success("Rasa project is ready for deployment!")
                    deploy(name)
                    # st.experimental_rerun()






if __name__ == '__main__':
    main()