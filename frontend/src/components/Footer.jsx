import { BsLinkedin, BsGithub } from "react-icons/bs";
import { HiOutlineMail } from "react-icons/hi";
import { motion } from "framer-motion";

function CustomFooter() {
  return (
    <footer className="fixed bottom-0 left-0 w-full bg-gradient-to-r from-black via-gray-900 to-black text-white shadow-md ">
      <div className="max-w-screen-xl mx-auto flex items-center justify-between px-6 py-4">
        <p className="text-sm text-[#a3a3a3] font-inter">
          © {new Date().getFullYear()}{" "}
          <a href="#" className="hover:underline">
            InsightGenei.ai
          </a>
        </p>
        <div className="flex space-x-6">
          <motion.a
            whileHover={{ scale: 1.2 }}
            whileTap={{ scale: 0.8 }}
            href="https://www.linkedin.com/in/roshan-kumar-singh-60b68a253/"
            target="_blank"
            rel="noopener noreferrer"
            className="text-[#2563eb] hover:text-[#ffffff]"
            aria-label="LinkedIn"
          >
            <BsLinkedin size={20} />
          </motion.a>
          <motion.a
            whileHover={{ scale: 1.4 }}
            whileTap={{ scale: 1.0 }}
            href="https://github.com/Roshansingh9/insightgenei.ai"
            target="_blank"
            rel="noopener noreferrer"
            className="text-[#2563eb] hover:text-[#ffffff]"
            aria-label="GitHub"
          >
            <BsGithub size={20} />
          </motion.a>
          <motion.a
            whileHover={{ scale: 1.7 }}
            whileTap={{ scale: 1.2 }}
            href="mailto:roshan.kr.singh9857@gmail.com"
            className="text-[#2563eb] hover:text-[#ffffff]"
            aria-label="Email"
          >
            <HiOutlineMail size={22} />
          </motion.a>
        </div>
      </div>
    </footer>
  );
}

export default CustomFooter;
