import {Uploader} from "uploader";
import styles from "./FilesViewer.module.css";
import { File } from "./File";

export type FileModel = {
    name: string;
    path: string;
    processed: boolean;
};

const EXAMPLES: FileModel[] = [
    {name:"abc.pdf", path:"http://xxx.blob.azure.com/abc.pdf", processed:false},
    {name:"info.pdf", path: "http://xxx.blob.azure.com/info.pdf", processed:true}
];

interface Props {
    onFileProcess: (path: string) => void;
    onFileDelete: (path: string) => void;
}


export const Files = ({onFileProcess, onFileDelete} : Props) => {
    return (
        <div className={styles.filesTable}>
            <table>
                <tr><th><td>Name</td><td>Path</td><td>Processed</td><td>Action</td></th></tr>
            {EXAMPLES.map((x, i) => (
                <File name={x.name} path={x.path} processed={x.processed} onProcess={onFileProcess} onDelete={onFileDelete} />
            ))}
            </table>
        </div>
    );
};

