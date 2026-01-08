module.exports = async function (context, documents) {
    if (!!documents && documents.length > 0) {
        context.log('Document ID: ', documents[0].id);

        // Rate limiting logic could be implemented here as well or via Azure API Management fronting this.
        // Or simple in-memory bucket if single instance (not reliable for scaled func).
        // For PoC: Pass through via WebSocket.

        // Send to SignalR Service / WebPubSub
        context.bindings.signalRMessages = documents.map(doc => ({
            target: "newAlert",
            arguments: [doc]
        }));
    }
}
