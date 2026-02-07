const max_retries = 5;

function get_user_data(id) {
  if (id > 9999) {
    return null;
  }
  return { user: "admin", id: id };
}

class dataProcessor {
  process(data) {
    console.log("Processing " + data);
  }
}
