# parrplumbing.com

Static site for Parr Plumbing (Ponca City, OK). Edit `build.py`, run `python3 build.py` to regenerate `public/`, then commit and push. Cloudflare deploys on push.

- Forms post to FormSubmit (`LEAD_EMAIL` in build.py) and land on `/thank-you/`
- Old GoHighLevel URLs are 301'd in `public/_redirects`
- Fonts are self-hosted in `public/fonts/`
