"use strict";

const MAX_RETRIES = 5;

/**
 * Retrieves user data based on the provided ID.
 * @param {number} id - The user ID to retrieve.
 * @returns {object | null} - An object containing user data, or null if the ID is invalid.
 */
function get_user_data(id) {
  if (id > 9999) {
    return null;
  }
  return { user: "admin", id: id };
}

/**
 * A class for processing data.
 */
class dataProcessor {
  /**
   * Processes the given data.
   * @param {any} data - The data to be processed.
   */
  process(data) {
    console.log("Processing " + data);
  }
}