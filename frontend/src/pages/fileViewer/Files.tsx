import styles from "./Files.module.css";
import {Uploader} from "uploader";
import { UploadDropzone  } from "react-uploader";
import { Files } from "../../components/FilesViewer/FilesViewer";

const uploader = Uploader({
    apiKey: "free"
})

const FilesViewer = () => {
    const uploaderOptions = {
        multi: true,
      
        // Comment out this line & use 'onUpdate' instead of
        // 'onComplete' to have the dropzone close after upload.
        showFinishButton: true,
      
        styles: {
          colors: {
            primary: "#377dff"
          }
        }
      }

    const onFileProcesse = (path: string) => {
        const response = fetch("/api/file", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({path})
        })

    }

    const onFileDelete = (path: string) => {
        const response = fetch("/api/file", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({path})
        })

    }

    return (
        <div className={styles.container}>
            <div className={styles.fileRoot}>
                <div className={styles.fileContainer}>
                    <Files onFileProcess={onFileProcesse} onFileDelete={onFileDelete} />
                </div>
                <div>
            
                <UploadDropzone uploader={uploader}
                  options={uploaderOptions}
                  onUpdate={(files: any[]) => console.log(files.map(x => x.fileUrl).join("\n"))}
                  onComplete={(files: any[]) => alert(files.map(x => x.fileUrl).join("\n"))}
                  width="600px"
                  height="375px" />
                </div>
            
            </div>
        </div>
    )
}

export default FilesViewer;