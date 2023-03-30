import { renderToStaticMarkup } from "react-dom/server";
import { getCitationFilePath } from "../../api";

type HtmlParsedAnswer = {
    answerHtml: string;
    citations: Citation[];
    followupQuestions: string[];
};

type Citation = {
    id: number;
    name: string;
    path: string;
};

export function parseAnswerToHtml(answer: string, onCitationClicked: (citationFilePath: string) => void): HtmlParsedAnswer {
    const citations: Citation[] = [];
    const followupQuestions: string[] = [];

    // Extract any follow-up questions that might be in the answer
    let parsedAnswer = answer.replace(/<<([^>>]+)>>/g, (match, content) => {
        followupQuestions.push(content);
        return "";
    });

    // trim any whitespace from the end of the answer after removing follow-up questions
    parsedAnswer = parsedAnswer.trim();

    // find information in string like '[info1.txt](http://www.example.com/info1.txt): info1' and extract info1.txt and http://www.example.com/info1.txt to be used as a link
    // parsedAnswer = parsedAnswer.replace(/\[([^\]]+)\]\(([^\)]+)\)/g, (match, content, url) => {
    //     const path = getCitationFilePath(content);
    //     return renderToStaticMarkup(
    //         <a className="supContainer" title={content} onClick={() => onCitationClicked(path)}>
    //             {content}
    //         </a>
    //     );
    // });


    // const parts = parsedAnswer.split(/\[([^\]]+)\]/g);
    const parts = parsedAnswer.split(/\[([^\]]+)\]+\(([^\)]+)\)/g);
    // const part_paths = parsedAnswer.split(/\(([^\)]+)\)/g);

    console.log(parts);

    let citation_map = parsedAnswer.match(/\[([^\]]+)\]+\(([^\)]+)\)/g) ;
    console.log(citation_map);

    citation_map ? citation_map.map((citation, index) => {
        const name = citation.split("]")[0].replace("[", "");
        const path = citation.split("]")[1].replace("(", "").replace(")", "");
        console.log(name);
        console.log(path);
        citations.push({
            id: index,
            name: name,
            path: path
        });
    }) : [];

    const fragments: string[] = parts.map((part, index) => {
        if (index % 3 === 0) {
            return part;
        } else if(index % 3 == 1){
            // let citationIndex: number;
            let cite = citations.find((citation) => citation.name == part);

            let citationIndex = cite? cite.id : -1;

            if (citationIndex !== -1) {
                citationIndex = cite ? cite.id + 1 : -1;
            } else {
                // citations.push(part);
                citationIndex = citations.length;
            }

            // console.log(parts);

            const path = getCitationFilePath(part);

            return renderToStaticMarkup(
                <a className="supContainer" title={part} onClick={() => onCitationClicked(path)}>
                    <sup>{citationIndex}</sup>
                </a>
            );
        } else{
            return "";
        }
    });

    return {
        answerHtml: fragments.join(""),
        citations,
        followupQuestions
    };
}
