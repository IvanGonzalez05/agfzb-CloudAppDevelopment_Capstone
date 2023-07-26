/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

// async function main(params) {
//       const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
//       const cloudant = CloudantV1.newInstance({
//           authenticator: authenticator
//       });
//       cloudant.setServiceUrl(params.COUCH_URL);

//       try {
//         let dbList = await cloudant.getAllDbs();
//         return { "dbs": dbList.result };
//       } catch (error) {
//           console.log(error)
//           return { error: error.description };
//       }
// }

async function main(params) {
    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
      const cloudant = CloudantV1.newInstance({
          authenticator: authenticator
      });
      cloudant.setServiceUrl(params.COUCH_URL);

      try {
          const dealerships = await cloudant.postAllDocs({ db: 'dealerships', includeDocs: true });
          return JSON.stringify({ body: dealerships.result.rows });
      } catch (error) {
          return { error: error.result };
      }
}