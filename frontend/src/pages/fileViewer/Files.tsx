import styles from "./Files.module.css";
import { Files, DataGrid } from "../../components/FilesViewer/FilesViewer";

const FilesViewer = () => {
    return (
        <div>
            <div>
                <div className={styles.filesViewer}>
                    <DataGrid/>
                </div>
                {/* <div>
            
                <UploadDropzone uploader={uploader}
                  options={uploaderOptions}
                  onUpdate={(files: any[]) => console.log(files.map(x => x.fileUrl).join("\n"))}
                  onComplete={(files: any[]) => alert(files.map(x => x.fileUrl).join("\n"))}
                  width="600px"
                  height="375px" />
                </div> */}
            
            </div>
        </div>
    )
}

export default FilesViewer;