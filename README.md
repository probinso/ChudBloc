Notice: This project is WIP

# ChudBloc

People are often using services like twitter to push notifications for live
participation and events. In some cases these communities have safety related
privacy concerns. These communities either need a private account
(limiting their reach), or have a robust blocklist to prevent bad actors from
intercepting content and producing harm. Both of these cases are subject to
much user error.

ChudBloc is a tool that will make it easier to identify potential bad actors.
We do this by propagating accounts' blocklist status within trusted communities.
This is done without sharing entire lists and doesn't allow for detailed
justifications in blocking. This is to prevent blocklists from becoming weapons
themselves. This is done by limiting users' blocked labels to
- `referred`
- `safety_concern`
- `personal_reason`

Tghe propagation model will allow users to specify `trusted_peers', for when
auditing of their blocklist's overlap with a peer's follow list, are notified
with an accumulation of blocked labels provided
(without making obvious who has provided which reasons).

There are ways in this model to slowly determine a user's complete blocklist,
however my intention is for that task to be sufficiently obnoxious rather than
secure. Additionally, blocks on twitter are mantained in propogation.
