// Sends http:// and www. traffic to https://parrplumbing.com, then serves the static site.
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.protocol === "http:" || url.hostname === "www.parrplumbing.com") {
      url.protocol = "https:";
      url.hostname = "parrplumbing.com";
      return Response.redirect(url.toString(), 301);
    }
    return env.ASSETS.fetch(request);
  },
};
