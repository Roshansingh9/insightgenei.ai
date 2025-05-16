import  { useState } from "react";
import Button from "./Button/Button";
import InfoModal from "./Button/Button_navigation"; 



const Header = () => {
  const [showModal, setShowModal] = useState(false);
  const [modalContent, setModalContent] = useState({
    title: "",
    description: "",
  });

  const openModal = (title, description) => {
    setModalContent({ title, description });
    setShowModal(true);
  };

  return (
    <header className="fixed top-0 left-0 w-full bg-gradient-to-r from-black via-gray-900 to-black text-white shadow-md z-50">
      <div className="max-w-screen-xl mx-auto flex items-center justify-between px-6 py-4">
        <img src="/logo-design.svg" alt="logo" className="h-10" />

        <div className="flex space-x-4">
          <Button
            title="How to use?"
            onClick={() =>
              openModal(
                "How to use this AI Platform",
                `1. Ask questions naturally:
              No need to know SQL — just type your query in any language (we support all languages!). For example, “Which brand has the highest average resale value?”
              
              2. Instant answers:
              Our AI converts your question into a database query and fetches accurate, up-to-date results instantly.
              
              3. Clear insights:
              Complex data is summarized and explained simply, so you get meaningful answers without sifting through raw data.
              
              4. Multilingual support:
              Interact effortlessly in English, Hindi, Spanish, or any language you prefer.`
              )
            }
          />
          <Button
            title="About Me"
            onClick={() =>
              openModal(
                "About Me",
                `Hi, I’m Roshan Kumar Singh, an undergraduate student passionate about exploring the endless possibilities of Artificial Intelligence and Generative AI. I love turning complex ideas into practical, impactful solutions that can help people and businesses thrive.

Whether it’s diving into the mysteries of machine learning and AI, unraveling the secrets of the cosmos, getting lost in the worlds of anime, cinema, and books, or pondering life’s biggest questions, I’m endlessly curious and always eager to explore.

If you’re into deep conversations about the vast unknowns of the universe, mind-bending math, or just want to geek out over anime, movies, books, and cutting-edge tech, let’s connect! You’ll find my socials in the footer of this webpage. Life’s way too short and weird not to nerd out about everything. So don’t hesitate — reach out, and let’s unravel the mysteries of existence (or at least argue about them).`
              )
            }
          />
        </div>
      </div>

      <InfoModal
        show={showModal}
        onClose={() => setShowModal(false)}
        title={modalContent.title}
        description={modalContent.description}
      />
    </header>
  );
};

export default Header;
