import { Container } from "@cloudflare/containers";

export class SummarizerContainer extends Container {
    defaultPort = 7860;
    sleepAfter = "10m";
}

export default {
    async fetch(request: Request, env: any) {
        const container = env.SUMMARIZER.getByName("summarizer");
        return container.fetch(request);
    }
};