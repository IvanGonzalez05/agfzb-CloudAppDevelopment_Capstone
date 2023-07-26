/**
 * Get dealerships by state
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
      const cloudant = CloudantV1.newInstance({
          authenticator: authenticator
      });
      cloudant.setServiceUrl(params.COUCH_URL);

      try {
          const dealerships = await cloudant.postFind({ db: 'dealerships', selector: params.selector });
          console.log(dealerships.result.docs)
          return JSON.stringify({ body: dealerships.result.docs });
      } catch (error) {
          return { error: error.result };
      }
}