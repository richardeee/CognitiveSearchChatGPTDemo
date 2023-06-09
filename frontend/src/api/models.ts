export const enum Approaches {
    RetrieveThenRead = "rtr",
    ReadRetrieveRead = "rrr",
    ReadDecomposeAsk = "rda"
}

export const enum CustomApproaches {
    BingSearch = "bing"
}

export type AskRequestOverrides = {
    semanticRanker?: boolean;
    semanticCaptions?: boolean;
    excludeCategory?: string;
    top?: number;
    temperature?: number;
    promptTemplate?: string;
    promptTemplatePrefix?: string;
    promptTemplateSuffix?: string;
    suggestFollowupQuestions?: boolean;
    useBingSearch?: boolean;
};

export type AskRequest = {
    question: string;
    approach: Approaches;
    overrides?: AskRequestOverrides;
};

export type AskResponse = {
    answer: string;
    thoughts: string | null;
    data_points: string;
    error?: string;
};

export type AskBingRequest = {
    question: string;
    approach: CustomApproaches;
    overrides?: AskRequestOverrides;
};

export type AskBingResponse = {
    answer: string;
    thoughts: string | null;
    data_points: string[];
    error?: string;
};


export type ChatTurn = {
    user: string;
    bot?: string;
};

export type ChatRequest = {
    history: ChatTurn[];
    approach: Approaches;
    overrides?: AskRequestOverrides;
};

export type ReadRequest = {
    answer: string;
}

export type File = {
    fileName: string;
    filePath: string;
    parsed: boolean;
}