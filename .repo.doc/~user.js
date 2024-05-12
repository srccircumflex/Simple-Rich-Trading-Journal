/*

source:	https://support.mozilla.org/de/questions/1264779


======================================================================================================================================================
The Policy/GPO way (Firefox 68)
-------------------------------

LocalFileLinks policy configuration: 			https://github.com/mozilla/policy-templates#localfilelinks

Customizing Firefox Using Group Policy (Windows): 	https://support.mozilla.org/en-US/kb/customizing-firefox-using-group-policy-windows
Customizing Firefox Using policies.json:		https://support.mozilla.org/en-US/kb/customizing-firefox-using-policiesjson

======================================================================================================================================================
The old proven method, which is backwards compatible, is to place this file as < user.js > in the current Firefox profile directory.
======================================================================================================================================================
*/

// == FILE URI LINK POLICY (checkloaduri) ==

// Create policy enabling http: or https: pages to link to file:
user_pref("capability.policy.policynames", "filelinks");
user_pref("capability.policy.filelinks.checkloaduri.enabled", "allAccess");

// Sites to which the policy applies (protocol://hostname protocol://hostname)
user_pref("capability.policy.filelinks.sites", "http://127.0.0.1:8050/");

