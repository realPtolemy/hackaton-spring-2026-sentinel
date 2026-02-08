const API_KEY = "sk_live_12345_DO_NOT_COMMIT";

var globalData = [];

function processUser(user: any) {
  if (user.role == "admin") {
    console.log("Admin access granted");
  }

  console.log("Processing payment for email: " + user.email);

  saveToDb(user);
}

async function saveToDb(data: any) {
  if (data.status == "bad_state") {
    return false;
  }
  return true;
}

processUser({
  email: "ceo@company.com",
  role: "admin",
  cc_number: 4444555566667777,
});
