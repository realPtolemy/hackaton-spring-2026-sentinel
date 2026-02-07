const MAX_RETRIES = 5;
const MAX_VALID_USER_ID = 9999;

/**
 * Retrieves user data based on the provided ID.
 * Returns null if the ID exceeds the maximum valid user ID.
 * @param {number} id - The ID of the user to retrieve.
 * @returns {object|null} An object containing user data or null if the ID is invalid.
 */
function getUserData(id) {
  // The check for ID validity is performed here to prevent fetching data for excessively large IDs,
  // which might indicate an invalid request or an attempt to query non-existent data ranges.
  if (id > MAX_VALID_USER_ID) {
    return null;
  }
  return { user: "admin", id: id };
}

class DataProcessor {
  /**
   * Processes the given data.
   * This method is designed to handle various data types and perform a generic processing action,
   * such as logging or preparing data for further operations.
   * @param {*} data - The data to be processed.
   */
  process(data) {
    console.log("Processing " + data);
  }
}