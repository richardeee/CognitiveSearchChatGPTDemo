import { useState, useEffect } from "react";
import { Stack, TextField } from "@fluentui/react";
import { Send28Filled, BookOpenMicrophone28Regular } from "@fluentui/react-icons";
import {SpeechConfig, AudioConfig, CancellationDetails, ResultReason, SpeechRecognizer, CancellationReason} from "microsoft-cognitiveservices-speech-sdk"
import styles from "./QuestionInput.module.css";

interface Props {
    onSend: (question: string) => void;
    disabled: boolean;
    placeholder?: string;
    clearOnSend?: boolean;
}

export const QuestionInput = ({ onSend, disabled, placeholder, clearOnSend }: Props) => {
    const [question, setQuestion] = useState<string>("");

    const sendQuestion = () => {
        if (disabled || !question.trim()) {
            console.log('send disabled');
            console.log('question: ' + question);
            return;
        }

        onSend(question);

        if (clearOnSend) {
            setQuestion("");
        }
    };

    const speechToText = () => {
        const speech_key = "e985cb0392ad45d59681a396b208ebcf"
        const speech_region = "southcentralus"
        var speechConfig = SpeechConfig.fromSubscription(speech_key,speech_region);
        const audioConfig = AudioConfig.fromDefaultMicrophoneInput();
        speechConfig.speechRecognitionLanguage = "zh-CN";
        const speechRecognizer = new SpeechRecognizer(speechConfig, audioConfig);
        speechRecognizer.recognizeOnceAsync(result => {
            switch (result.reason) {
                case ResultReason.RecognizedSpeech:
                    console.log(`RECOGNIZED: Text=${result.text}`);
                    setQuestion(result.text);
                    break;
                case ResultReason.NoMatch:
                    console.log("NOMATCH: Speech could not be recognized.");
                    break;
                case ResultReason.Canceled:
                    const cancellation = CancellationDetails.fromResult(result);
                    console.log(`CANCELED: Reason=${cancellation.reason}`);
    
                    if (cancellation.reason == CancellationReason.Error) {
                        console.log(`CANCELED: ErrorCode=${cancellation.ErrorCode}`);
                        console.log(`CANCELED: ErrorDetails=${cancellation.errorDetails}`);
                        console.log("CANCELED: Did you set the speech resource key and region values?");
                    }
                    break;
            }
            speechRecognizer.close();
        });
    }
    const onEnterPress = (ev: React.KeyboardEvent<Element>) => {
        if (ev.key === "Enter" && !ev.shiftKey) {
            ev.preventDefault();
            sendQuestion();
        }
    };

    const onQuestionChange = (_ev: React.FormEvent<HTMLInputElement | HTMLTextAreaElement>, newValue?: string) => {
        if (!newValue) {
            setQuestion("");
        } else if (newValue.length <= 1000) {
            setQuestion(newValue);
        }
    };

    const sendQuestionDisabled = disabled || !question.trim();

    return (
        <Stack horizontal className={styles.questionInputContainer}>
            <TextField
                className={styles.questionInputTextArea}
                placeholder={placeholder}
                multiline
                resizable={false}
                borderless
                value={question}
                onChange={onQuestionChange}
                onKeyDown={onEnterPress}
            />
            <div className={styles.questionInputButtonsContainer}>
                <div
                    className={`${styles.questionInputSendButton} ${sendQuestionDisabled ? styles.questionInputSendButtonDisabled : ""}`}
                    aria-label="语音输入"
                    onClick={speechToText}
                >
                    <BookOpenMicrophone28Regular primaryFill="rgba(115, 118, 225, 1)" />
                </div>
                <div
                    className={`${styles.questionInputSendButton} ${sendQuestionDisabled ? styles.questionInputSendButtonDisabled : ""}`}
                    aria-label="提问按钮"
                    onClick={sendQuestion}
                >
                    <Send28Filled primaryFill="rgba(115, 118, 225, 1)" />
                </div>
            </div>
        </Stack>
    );
};
