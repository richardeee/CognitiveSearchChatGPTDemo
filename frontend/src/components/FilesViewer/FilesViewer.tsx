import { Uploader } from "uploader";
import styles from "./FilesViewer.module.css";
import { File } from "./File";
import { UploadDropzone } from "react-uploader";
import { useRef, useState, useEffect } from "react";

const uploader = Uploader({
    apiKey: "free"
});

import {
    TableBody,
    TableCell,
    TableRow,
    Table,
    TableHeader,
    TableHeaderCell,
    TableSelectionCell,
    TableCellLayout,
    useTableFeatures,
    TableColumnDefinition,
    useTableSelection,
    useTableSort,
    createTableColumn,
    TableColumnId,
    PresenceBadgeStatus,
    Avatar,
    useArrowNavigationGroup,
    webLightTheme,
    FluentProvider,
    Button,
    Dialog,
    DialogTrigger,
    DialogSurface,
    DialogTitle,
    DialogBody,
    DialogActions,
    DialogContent,
    Text
} from "@fluentui/react-components";
import * as React from "react";
import {
    FolderRegular,
    EditRegular,
    OpenRegular,
    DocumentRegular,
    PeopleRegular,
    DocumentPdfRegular,
    VideoRegular,
    ArrowUploadRegular
} from "@fluentui/react-icons";
import { getFileTypeIconProps, FileIconType } from "@fluentui/react-file-type-icons";

type FileCell = {
    label: string;
    icon: JSX.Element;
};

type LastUpdatedCell = {
    label: string;
    timestamp: number;
};

type LastUpdateCell = {
    label: string;
    icon: JSX.Element;
};

type AuthorCell = {
    label: string;
    status: PresenceBadgeStatus;
};

type PathCell = {
    label: string;
};

type Item = {
    file: FileCell;
    author: AuthorCell;
    lastUpdated: LastUpdatedCell;
    lastUpdate: LastUpdateCell;
    filePath: PathCell;
};

const items: Item[] = [
    {
        file: { label: "Meeting notes", icon: <DocumentRegular /> },
        author: { label: "Max Mustermann", status: "available" },
        lastUpdated: { label: "7h ago", timestamp: 3 },
        lastUpdate: {
            label: "You edited this",
            icon: <EditRegular />
        },
        filePath: { label: "http://xxx.blob.azure.com/abc.pdf" }
    },
    {
        file: { label: "Thursday presentation", icon: <FolderRegular /> },
        author: { label: "Erika Mustermann", status: "busy" },
        lastUpdated: { label: "Yesterday at 1:45 PM", timestamp: 2 },
        lastUpdate: {
            label: "You recently opened this",
            icon: <OpenRegular />
        },
        filePath: { label: "http://xxx.blob.azure.com/abc.pdf" }
    },
    {
        file: { label: "Training recording", icon: <VideoRegular /> },
        author: { label: "John Doe", status: "away" },
        lastUpdated: { label: "Yesterday at 1:45 PM", timestamp: 2 },
        lastUpdate: {
            label: "You recently opened this",
            icon: <OpenRegular />
        },
        filePath: { label: "http://xxx.blob.azure.com/abc.pdf" }
    },
    {
        file: { label: "Purchase order", icon: <DocumentPdfRegular /> },
        author: { label: "Jane Doe", status: "offline" },
        lastUpdated: { label: "Tue at 9:30 AM", timestamp: 1 },
        lastUpdate: {
            label: "You shared this in a Teams chat",
            icon: <PeopleRegular />
        },
        filePath: { label: "http://xxx.blob.azure.com/abc.pdf" }
    }
];

const columns: TableColumnDefinition<Item>[] = [
    createTableColumn<Item>({
        columnId: "file",
        compare: (a: { file: { label: string } }, b: { file: { label: string } }) => {
            return a.file.label.localeCompare(b.file.label);
        }
    }),
    createTableColumn<Item>({
        columnId: "author",
        compare: (a: { author: { label: string } }, b: { author: { label: string } }) => {
            return a.author.label.localeCompare(b.author.label);
        }
    }),
    createTableColumn<Item>({
        columnId: "lastUpdated",
        compare: (a: { lastUpdated: { timestamp: number } }, b: { lastUpdated: { timestamp: number } }) => {
            return a.lastUpdated.timestamp - b.lastUpdated.timestamp;
        }
    }),
    createTableColumn<Item>({
        columnId: "lastUpdate",
        compare: (a: { lastUpdate: { label: string } }, b: { lastUpdate: { label: any } }) => {
            return a.lastUpdate.label.localeCompare(b.lastUpdate.label);
        }
    }),
    createTableColumn<Item>({
        columnId: "filePath",
        compare: (a: { filePath: { label: string } }, b: { filePath: { label: any } }) => {
            return a.filePath.label.localeCompare(b.filePath.label);
        }
    })
];

export const DataGrid = () => {
    const [selectedRows, setSelectedRows] = useState(new Set([]));
    const {
        getRows,
        selection: { allRowsSelected, someRowsSelected, toggleAllRows, toggleRow, isRowSelected },
        sort: { getSortDirection, toggleColumnSort, sort }
    } = useTableFeatures(
        {
            columns,
            items
        },
        [
            useTableSelection({
                selectionMode: "multiselect",
                defaultSelectedItems: new Set([]),
            }),
            useTableSort({
                defaultSortState: { sortColumn: "file", sortDirection: "ascending" }
            })
        ]
    );

    const rows = sort(
        getRows(row => {
            const selected = isRowSelected(row.rowId);
            return {
                ...row,
                onClick: (e: React.MouseEvent) => toggleRow(e, row.rowId),
                onKeyDown: (e: React.KeyboardEvent) => {
                    if (e.key === " ") {
                        e.preventDefault();
                        toggleRow(e, row.rowId);
                    }
                },
                selected,
                appearance: selected ? ("brand" as const) : ("none" as const)
            };
        })
    );

    const headerSortProps = (columnId: TableColumnId) => ({
        onClick: (e: React.MouseEvent) => {
            toggleColumnSort(e, columnId);
        },
        sortDirection: getSortDirection(columnId)
    });

    const keyboardNavAttr = useArrowNavigationGroup({ axis: "grid" });

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
    };

    return (
        <div className={styles.container}>
            <FluentProvider theme={webLightTheme}>
                <Table {...keyboardNavAttr} role="grid" sortable aria-label="DataGrid implementation with Table primitives">
                    <TableHeader>
                        <TableRow>
                            <TableSelectionCell
                                checked={allRowsSelected ? true : someRowsSelected ? "mixed" : false}
                                aria-checked={allRowsSelected ? true : someRowsSelected ? "mixed" : false}
                                role="checkbox"
                                onClick={toggleAllRows}
                                checkboxIndicator={{ "aria-label": "Select all rows " }}
                            />

                            <TableHeaderCell {...headerSortProps("file")}>File</TableHeaderCell>
                            <TableHeaderCell {...headerSortProps("author")}>Author</TableHeaderCell>
                            <TableHeaderCell {...headerSortProps("lastUpdated")}>Last updated</TableHeaderCell>
                            <TableHeaderCell {...headerSortProps("lastUpdate")}>Last update</TableHeaderCell>
                            <TableHeaderCell {...headerSortProps("filePath")}>Path</TableHeaderCell>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {rows.map(({ item, selected, onClick, onKeyDown, appearance }) => (
                            <TableRow key={item.file.label} onClick={onClick} onKeyDown={onKeyDown} aria-selected={selected} appearance={appearance}>
                                <TableSelectionCell
                                    role="gridcell"
                                    aria-selected={selected}
                                    checked={selected}
                                    checkboxIndicator={{ "aria-label": "Select row" }}
                                />

                                <TableCell tabIndex={0} role="gridcell" aria-selected={selected}>
                                    <TableCellLayout media={item.file.icon}>{item.file.label}</TableCellLayout>
                                </TableCell>
                                <TableCell tabIndex={0} role="gridcell">
                                    <TableCellLayout
                                        media={<Avatar aria-label={item.author.label} name={item.author.label} badge={{ status: item.author.status }} />}
                                    >
                                        {item.author.label}
                                    </TableCellLayout>
                                </TableCell>
                                <TableCell tabIndex={0} role="gridcell">
                                    {item.lastUpdated.label}
                                </TableCell>
                                <TableCell tabIndex={0} role="gridcell">
                                    <TableCellLayout media={item.lastUpdate.icon}>{item.lastUpdate.label}</TableCellLayout>
                                </TableCell>
                                <TableCell tabIndex={0} role="gridcell">
                                    <TableCellLayout>{item.filePath.label}</TableCellLayout>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
                <div className={styles.processButtonGroup}>
                    <Dialog>
                        <DialogTrigger disableButtonEnhancement>
                            <Button>处理选中文档</Button>
                        </DialogTrigger>
                        <DialogSurface>
                            <DialogTitle>处理选中文档</DialogTitle>
                            <DialogBody>
                                <Text>确认处理选中文档? 这将重新处理选中文档。</Text>
                            </DialogBody>
                            <DialogActions>
                                <DialogTrigger disableButtonEnhancement>
                                    <Button appearance="secondary">取消</Button>
                                </DialogTrigger>
                                <Button appearance="primary" >确认</Button>
                            </DialogActions>
                        </DialogSurface>
                    </Dialog>
                    <Dialog>
                        <DialogTrigger disableButtonEnhancement>
                            <Button>处理全部文档</Button>
                        </DialogTrigger>
                        <DialogSurface>
                            <DialogTitle>处理全部文档</DialogTitle>
                            <DialogBody>
                                <Text>确认处理全部文档? 这将重新处理全部文档。</Text>
                            </DialogBody>
                            <DialogActions>
                                <DialogTrigger disableButtonEnhancement>
                                    <Button appearance="secondary">取消</Button>
                                </DialogTrigger>
                                <Button appearance="primary">确认</Button>
                            </DialogActions>
                        </DialogSurface>
                    </Dialog>
                    <Dialog>
                        <DialogTrigger disableButtonEnhancement>
                            <Button icon={<ArrowUploadRegular />}>上传新文档</Button>
                        </DialogTrigger>
                        <DialogSurface>
                            <DialogTitle>上传新文档</DialogTitle>
                            <DialogBody>
                                <UploadDropzone
                                    uploader={uploader}
                                    options={uploaderOptions}
                                    onUpdate={(files: any[]) => console.log(files.map(x => x.fileUrl).join("\n"))}
                                    onComplete={(files: any[]) => alert(files.map(x => x.fileUrl).join("\n"))}
                                    width="600px"
                                    height="375px"
                                />
                            </DialogBody>
                            <DialogActions>
                                <DialogTrigger disableButtonEnhancement>
                                    <Button appearance="secondary">取消</Button>
                                </DialogTrigger>
                                <Button appearance="primary">确认</Button>
                            </DialogActions>
                        </DialogSurface>
                    </Dialog>
                </div>
            </FluentProvider>
        </div>
    );
};

export type FileModel = {
    name: string;
    path: string;
    processed: boolean;
};

const EXAMPLES: FileModel[] = [
    { name: "abc.pdf", path: "http://xxx.blob.azure.com/abc.pdf", processed: false },
    { name: "info.pdf", path: "http://xxx.blob.azure.com/info.pdf", processed: true }
];

interface Props {
    onFileProcess: (path: string) => void;
    onFileDelete: (path: string) => void;
}

export const Files = ({ onFileProcess, onFileDelete }: Props) => {
    return (
        <div className={styles.filesTable}>
            <table>
                <tr>
                    <th>
                        <td>Name</td>
                        <td>Path</td>
                        <td>Processed</td>
                        <td>Action</td>
                    </th>
                </tr>
                {EXAMPLES.map((x, i) => (
                    <File name={x.name} path={x.path} processed={x.processed} onProcess={onFileProcess} onDelete={onFileDelete} />
                ))}
            </table>
        </div>
    );
};
