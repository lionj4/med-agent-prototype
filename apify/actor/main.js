// Apify actor template (Node.js). Purpose: crawl public drug data and output normalized JSON.
// Minimal template: adapt selectors and sources for DailyMed / RxNorm.
const Apify = require('apify');

Apify.main(async () => {
    const requestQueue = await Apify.openRequestQueue();
    await requestQueue.addRequest({ url: 'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=example' });

    const dataset = await Apify.openDataset();

    const handlePageFunction = async ({ request, $ }) => {
        const title = $('title').text();
        const item = {
            drug_name_en: title,
            source_url: request.url,
        };
        await dataset.pushData(item);
    };

    const crawler = new Apify.CheerioCrawler({
        requestQueue,
        handlePageFunction,
    });

    await crawler.run();
});
