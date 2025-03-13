const express = require("express");
const { register, login, dashboard } = require("../controllers/authController");
const verifyToken = require("../middlewares/authMiddleware");

const router = express.Router();

router.post("/register", register);
router.post("/login", login);
router.get("/dashboard", verifyToken, dashboard);

module.exports = router;
