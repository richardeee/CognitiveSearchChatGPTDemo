import { Example } from "./Example";

import styles from "./Example.module.css";

export type ExampleModel = {
    text: string;
    value: string;
};

const EXAMPLES: ExampleModel[] = [
    {
        text: "试剂盘有异响是什么原因，怎么解决?",
        value: "试剂盘有异响是什么原因，怎么解决?"
    },
    { text: "建立真空失败是什么原因？怎么解决", value: "建立真空失败是什么原因？怎么解决" },
    { text: "面壳的下单编码和物料名称有哪些", value: "面壳的下单编码和物料名称有哪些" }
];

interface Props {
    onExampleClicked: (value: string) => void;
}

export const ExampleList = ({ onExampleClicked }: Props) => {
    return (
        <ul className={styles.examplesNavList}>
            {EXAMPLES.map((x, i) => (
                <li key={i}>
                    <Example text={x.text} value={x.value} onClick={onExampleClicked} />
                </li>
            ))}
        </ul>
    );
};
