import { motion } from "framer-motion";

const Button = ({ title, onClick }) => {
  return (
    <motion.button
      onClick={onClick}
      whileHover={{ scale: 1.2 }}
      whileTap={{ scale: 0.8 }}
      className="px-4 py-2 rounded-md bg-gradient-to-r from-teal-600 to-blue-600 text-white"
    >
      {title}
    </motion.button>
  );
};

export default Button;
