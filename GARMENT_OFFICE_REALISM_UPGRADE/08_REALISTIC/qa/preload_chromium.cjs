// Select the installed Chromium; the repository tests themselves remain unchanged.
const {chromium}=require('playwright');
const original=chromium.launch.bind(chromium);
chromium.launch=(options={})=>original({...options,executablePath:'/usr/bin/chromium',args:['--no-sandbox',...(options.args||[])]});
