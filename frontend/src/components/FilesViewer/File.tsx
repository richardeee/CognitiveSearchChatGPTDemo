import { Check, IconButton } from "@fluentui/react";
import styles from "./FilesViewer.module.css";

interface Props {
    name: string;
    path: string;
    processed: boolean;
    onProcess: (path: string) => void;
    onDelete: (path: string) => void;
}

export const File = ({ name, path, processed, onProcess, onDelete }: Props) => {
    return (
        <tr className={styles.file}>
            <td>{name}</td>
            <td><Check checked={processed}></Check></td>
            <td><span>{path}</span></td>
            <td>
            <IconButton iconProps={{ iconName: "Processing" }} onClick={() => onProcess(path)}></IconButton>
            <IconButton iconProps={{ iconName: "Delete" }} onClick={() => onDelete(path)}></IconButton>
            </td>
        </tr>
    );
};
