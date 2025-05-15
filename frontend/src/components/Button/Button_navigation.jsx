import { motion, AnimatePresence } from "framer-motion";
import { IoClose } from "react-icons/io5";
import { useState, useEffect } from "react";

const InfoModal = ({ show, onClose, title, description }) => {
  // Track if modal is being hovered
  const [isHovered, setIsHovered] = useState({
    title: false,
    description: false,
  });

  // Close on escape key
  useEffect(() => {
    const handleEsc = (e) => {
      if (e.key === "Escape" && show) {
        onClose();
      }
    };

    window.addEventListener("keydown", handleEsc);
    return () => window.removeEventListener("keydown", handleEsc);
  }, [show, onClose]);

  // Animation variants
  const backdropVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1 },
    exit: { opacity: 0 },
  };

  const modalVariants = {
    hidden: { opacity: 0, scale: 0.8, y: 40 },
    visible: {
      opacity: 1,
      scale: 1,
      y: 0,
      transition: {
        type: "spring",
        damping: 25,
        stiffness: 300,
      },
    },
    exit: {
      opacity: 0,
      scale: 0.9,
      y: 20,
      transition: { duration: 0.2 },
    },
  };

  const glassVariants = {
    rest: {
      boxShadow:
        "0 8px 32px rgba(13, 148, 136, 0.4), inset 0 0 20px rgba(13, 148, 136, 0.3)",
    },
    hover: {
      boxShadow:
        "0 8px 40px rgba(13, 148, 136, 0.55), inset 0 0 30px rgba(13, 148, 136, 0.4)",
    },
  };

  return (
    <AnimatePresence>
      {show && (
        <motion.div
          className="fixed inset-0 flex items-center justify-center z-50"
          initial="hidden"
          animate="visible"
          exit="exit"
          variants={backdropVariants}
          transition={{ duration: 0.3 }}
          onClick={onClose}
          style={{
            backgroundColor: "rgba(0, 0, 0, 0.75)",
            backdropFilter: "blur(3px)",
          }}
        >
          <motion.div
            className="relative mx-4 md:mx-auto max-w-3xl w-full"
            variants={modalVariants}
            onClick={(e) => e.stopPropagation()}
          >
            {/* Main modal container */}
            <div
              className="rounded-3xl overflow-hidden relative"
              style={{
                background:
                  "linear-gradient(145deg, rgba(15, 15, 15, 0.95), rgba(30, 30, 30, 0.85))",
                border: "1px solid rgba(255, 255, 255, 0.1)",
                boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.5)",
              }}
            >
              {/* Glow effect */}
              <div
                className="absolute inset-0 pointer-events-none"
                style={{
                  background:
                    "radial-gradient(circle at 50% 0%, rgba(13, 148, 136, 0.15), transparent 50%)",
                  zIndex: 0,
                }}
              />

              <div className="p-6 md:p-8 space-y-6 relative z-10">
                {/* Close Button */}
                <motion.button
                  className="absolute top-5 right-5 text-gray-400 hover:text-white z-20"
                  onClick={onClose}
                  aria-label="Close"
                  whileHover={{ scale: 1.1, rotate: 90 }}
                  whileTap={{ scale: 0.9 }}
                  transition={{ duration: 0.2 }}
                >
                  <IoClose size={26} />
                </motion.button>

                {/* Title Box */}
                <motion.div
                  className="rounded-xl overflow-hidden relative"
                  variants={glassVariants}
                  initial="rest"
                  animate={isHovered.title ? "hover" : "rest"}
                  onMouseEnter={() =>
                    setIsHovered({ ...isHovered, title: true })
                  }
                  onMouseLeave={() =>
                    setIsHovered({ ...isHovered, title: false })
                  }
                  transition={{ duration: 0.4 }}
                >
                  <div
                    className="px-6 py-5 text-center relative z-10"
                    style={{
                      background:
                        "linear-gradient(135deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.05) 100%)",
                      backdropFilter: "blur(15px)",
                      border: "1px solid rgba(255, 255, 255, 0.2)",
                      borderRadius: "12px",
                    }}
                  >
                    <h2 className="text-3xl font-bold bg-gradient-to-br from-teal-400 to-teal-600 bg-clip-text text-transparent">
                      {title}
                    </h2>

                    {/* Subtle animations for title box */}
                    <motion.div
                      className="absolute inset-0 pointer-events-none"
                      animate={{
                        background: isHovered.title
                          ? "linear-gradient(135deg, rgba(13, 148, 136, 0.2) 0%, rgba(13, 148, 136, 0.05) 100%)"
                          : "linear-gradient(135deg, rgba(13, 148, 136, 0.1) 0%, rgba(13, 148, 136, 0.02) 100%)",
                      }}
                      transition={{ duration: 0.6 }}
                    />
                  </div>
                </motion.div>

                {/* Description Box */}
                <motion.div
                  className="rounded-xl overflow-hidden relative"
                  variants={glassVariants}
                  initial="rest"
                  animate={isHovered.description ? "hover" : "rest"}
                  onMouseEnter={() =>
                    setIsHovered({ ...isHovered, description: true })
                  }
                  onMouseLeave={() =>
                    setIsHovered({ ...isHovered, description: false })
                  }
                  transition={{ duration: 0.4 }}
                >
                  <div
                    className="px-6 py-6 relative z-10"
                    style={{
                      background:
                        "linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.02) 100%)",
                      backdropFilter: "blur(12px)",
                      border: "1px solid rgba(255, 255, 255, 0.15)",
                      borderRadius: "12px",
                    }}
                  >
                    <p
                      className="text-gray-300 leading-relaxed"
                      style={{ whiteSpace: "pre-line" }}
                    >
                      {description}
                    </p>

                    {/* Subtle animations for description box */}
                    <motion.div
                      className="absolute inset-0 pointer-events-none"
                      animate={{
                        background: isHovered.description
                          ? "linear-gradient(135deg, rgba(13, 148, 136, 0.12) 0%, rgba(13, 148, 136, 0.02) 100%)"
                          : "linear-gradient(135deg, rgba(13, 148, 136, 0.05) 0%, rgba(13, 148, 136, 0.01) 100%)",
                      }}
                      transition={{ duration: 0.6 }}
                    />
                  </div>
                </motion.div>
              </div>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default InfoModal;
