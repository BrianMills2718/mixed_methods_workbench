export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/investigation/psychosisbank-disclosure") {
      url.pathname = "/api/investigation/psychosisbank-disclosure.json";
      return env.ASSETS.fetch(new Request(url, request));
    }
    return env.ASSETS.fetch(request);
  },
};
