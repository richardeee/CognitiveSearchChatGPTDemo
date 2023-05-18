import styles from "./Files.module.css";
import { Files, DataGrid } from "../../components/FilesViewer/FilesViewer";
import { ChangeEvent, useState } from 'react';

const FilesViewer = () => {
    
    const [file, setFile] = useState<File>()

    const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
          setFile(e.target.files[0]);
        }
      };

    const handleUploadFile = () => {
        if (!file) {
            return;
        }
    
        const data = new FormData();
    
        fetch('/uploadFile', {
          method: 'POST',
          body: file,
          headers: {
            'content-type': file.type,
            'content-length': `${file.size}`, // 👈 Headers need to be a string
          },
        }).then((response) => {
          response.json()
        }).then((data) => console.log(data))
        .then((err) => console.log(err))
      }

    return (
        <div>
            <div>
                <div className={styles.filesViewer}>
                    <DataGrid/>
                </div>
                <div>
                    <input type="file" onChange={handleFileChange} />
                    <div>{file && `${file.name} - ${file.type}`}</div>
                    <button onClick={handleUploadFile}>Upload</button>
                </div>
            
            </div>
        </div>
    )
}

export default FilesViewer;