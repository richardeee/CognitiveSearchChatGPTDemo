import { Example } from "./Example";

import styles from "./Example.module.css";

export type ExampleModel = {
    text: string;
    value: string;
};

const EXAMPLES: ExampleModel[] = [
    {
        text: "九节菖蒲与石菖蒲是同一植物吗?",
        value: "九节菖蒲与石菖蒲是同一植物吗?"
    },
    { text: "餐饮食品吃拉肚子想要做检测，有什么标准可依?", value: "餐饮食品吃拉肚子想要做检测，有什么标准可依?" },
    { text: "茶叶按9833.3测试冠突散囊菌，如何知道茶叶是否长毛?", value: "茶叶按9833.3测试冠突散囊菌，如何知道茶叶是否长毛?" }
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
