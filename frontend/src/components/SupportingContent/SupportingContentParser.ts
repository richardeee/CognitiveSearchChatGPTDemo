type ParsedSupportingContentItem = {
    title: string;
    content: string;
    url: string;
};

// export function parseSupportingContentItem(item: string): ParsedSupportingContentItem {
//     // Assumes the item starts with the file name followed by : and the content.
//     // Example: "sdp_corporate.pdf: this is the content that follows".
//     const parts = item.split(": ");
//     const title = parts[0];
//     var content = parts.slice(1).join(": ") ? parts.slice(1).join(": ") : "No content";
    
//     //Extrace string in '<>' in content, example: info1.txt: abc <http://www.google.com>
//     const url = content.match(/<([^>]+)>/);

//     //Replace string in '<>' in content, example: info1.txt: abc <http://www.google.com>
//     content = content.replace(/<([^>]+)>/g, "");
    
    

//     return {
//         title,
//         content,
//         url: url ? url[1] : ""
//     };
// }
export function parseSupportingContentItem(item: string): ParsedSupportingContentItem {
    // Assumes the item starts with the file name followed by : and the content.
    // Example: {"sourcepage": "sdp_corporate.pdf", "content": "this is the content that follows", "sourcepage_path":"http://www.sampledomain.com/sdp_corporate.pdf"}.
    const itemj = eval(item)

    const title = itemj.sourcepage;
    const content = itemj.content;
    const url = itemj.sourcepage_path;

    return {
        title,
        content,
        url: url ? url : ""
    };
}
