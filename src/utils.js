const MAX_RETRIES_ALLOWED = 5;
const MAX_VALID_USER_ID = 9999;

/**
 * Retrieves user data based on the provided ID.
 * @param {number} userId - The ID of the user to retrieve.
 * @returns {object | null} - An object containing user data if the ID is valid, otherwise null.
 */
function getUserData(userId) {
  // Check if the user ID exceeds the maximum allowed value.
  if (userId > MAX_VALID_USER_ID) {
    // Return null if the user ID is invalid.
    return null;
  }
  // Return user data if the user ID is valid.
  return { user: 'admin', id: userId };
}

/**
 * Class for processing data.
 */
class DataProcessor {
  /**
   * Processes the provided data.
   * @param {any} data - The data to be processed.
   */
  processData(data) {
    // Log the data being processed.
    console.log('Processing', data);
  }
}