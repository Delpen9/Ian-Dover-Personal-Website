import os
from flask_caching import Cache

from flask import (
    Flask,
    render_template,
    send_from_directory,
    request,
    redirect,
    url_for,
)

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import base64

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Needed for flashing messages

@app.route("/")
def bio():
    return render_template("bio.html")


@app.route("/timeline")
def timeline():
    projects = [
        {
            "date": "09-20-2024",
            "url": "https://github.com/Delpen9/Reinsurance-Case-Study/blob/main/case_study.pdf",
            "title": "Reinsurance Analysis",
        },
        {
            "date": "07-20-2024",
            "url": "https://github.com/Delpen9/Argentina-Inflation/blob/main/argentina_analysis_presentation.pdf",
            "title": "Argentina Inflation",
        },
        {
            "date": "07-10-2024",
            "url": "https://www.parchment.com/u/award/ef2f17b678782a1f5b2b442ea0231623",
            "title": "Georgia Tech Grad",
        },
        {
            "date": "07-01-2023",
            "url": "https://github.com/Delpen9/Ian-Dover-Personal-Website/tree/main",
            "title": "Portfolio Website",
        },
        {
            "date": "06-25-2023",
            "url": "https://github.com/Delpen9/Underwriting-Challenge",
            "title": "Underwriting Challenge",
        },
        {
            "date": "04-29-2023",
            "url": "https://github.com/Delpen9/optimization_methods_final",
            "title": "Optimization Methods",
        },
        {
            "date": "04-20-2023",
            "url": "https://github.com/Delpen9/data_compression_experiments",
            "title": "Data Compression",
        },
        {
            "date": "04-01-2023",
            "url": "https://github.com/Delpen9/lasso_ridge_elastic_group_optimization",
            "title": "Group Optimization",
        },
        {
            "date": "03-20-2023",
            "url": "https://github.com/Delpen9/Lagrangian-Optimization-Algorithms/tree/main",
            "title": "Descent Algorithms",
        },
    ]

    # Enforce title length
    for project in projects:
        if len(project["title"]) > 25:
            raise ValueError(f"Title '{project['title']}' exceeds 25 characters")

    return render_template("timeline.html", projects=projects)


def send_email(name, email, message):
    # Replace these with your actual email credentials
    sender_email = "iantdover@gmail.com"
    receiver_email = "iantdover@gmail.com"
    password = base64.b64decode(r"a2NvYyBueXpoIHdpeWQgY2R6cw==").decode('utf-8')

    # Set up the MIME
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "SOMEONE CONTACTED YOU ON IANDOVERPORTFOLIO.COM"

    # Create the body of the message
    body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
    msg.attach(MIMEText(body, "plain"))

    # Set up the server and send the email
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()


@app.route("/submit-form", methods=["POST"])
def submit_form():
    try:
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        send_email(name, email, message)
        return redirect(
            url_for("contact")
        )  # Redirects back to the contact page on successful email send
    except Exception as e:
        print(e)  # Optionally print the error to the console or log it
        return redirect(
            url_for("contact")
        )  # Redirects back to the contact page on error


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/resume")
def resume():
    return send_from_directory("static/content/resume", "Ian_Dover_Resume.pdf")


@app.route("/blog")
def blog():
    blog_posts = [
        {
            "title": "ML Model Ownership, Inference Slashing, and Seed Rounds on Crowd-Training Protocol",
            "content": "The Crowd Training Protocol introduces an innovative ownership model for machine learning, rewarding contributors based on their roles as ecosystem supporters, data providers, or computational resource contributors. By leveraging inference slashing, seed rounds, and ownership inflation, the protocol ensures equitable compensation, fosters collaboration, and sustains the development and maintenance of decentralized machine learning models.",
            "date": "January 21, 2025",
            "url": "https://medium.com/@iantdover/ml-model-ownership-inference-slashing-and-seed-rounds-on-crowd-training-protocol-8206ffdf5b81"
        },
        {
            "title": "Partial Privacy-Preserving ML Models on Crowd Training Protocol",
            "content": "The article explores a hybrid framework for addressing the machine learning trilemma—privacy preservation, computational efficiency, and model performance—by combining Fully Homomorphic Encryption (FHE) and Distributed Trusted Execution Environments (DTEEs).",
            "date": "January 19, 2025",
            "url": "https://medium.com/@iantdover/partial-privacy-preserving-ml-models-on-crowd-training-protocol-4c5b6e613320"
        },
        {
            "title": "Reverse Robin Hood Attacks and Crowd Training Protocol",
            "content": "The article examines the concept of 'Reverse Robin Hood Attacks,' where resources are extracted from less fortunate participants and funneled to wealthier entities, and its implications for the Crowd Training Protocol.",
            "date": "January 12, 2025",
            "url": "https://medium.com/@iantdover/reverse-robin-hood-attacks-and-crowd-training-protocol-25c14f88fac5"
        },
        {
            "title": "Crowd Training Protocol",
            "content": "The Crowd Training Protocol leverages blockchain technology and decentralized governance to enable collaborative training and management of machine learning models while ensuring transparency, fairness, and accountability.",
            "date": "January 12, 2025",
            "url": "https://medium.com/@iantdover/crowd-training-protocol-8ac8fd2faed6"
        },
        {
            "title": "Crowd-Training AI on the Blockchain: Private Weights, Public Architecture",
            "content": "This article explores how blockchain-enabled crowd training integrates decentralized AI development with collaborative governance, leveraging innovations like federated learning, compute-intensive smart contracts, and the Private Weights, Public Architecture (PWPA) paradigm.",
            "date": "January 10, 2025",
            "url": "https://medium.com/@iantdover/crowd-training-ai-on-the-blockchain-private-weights-public-architecture-aaa00ca92162"
        },
        {
            "title": "The Tokenomics of Internet Computer Protocol are Quite Good",
            "content": "The Internet Computer Protocol (ICP) tokenomics are designed to drive sustainable growth through mechanisms like cycle burning, developer demand, and staking rewards, which reduce supply and increase demand. With a built-in price floor tied to developer usage and the potential for deflation as ecosystem adoption grows, ICP offers a robust framework for long-term price stability and utility.",
            "date": "December 24, 2024",
            "url": "https://medium.com/@iantdover/the-tokenomics-of-internet-computer-protocol-are-quite-good-463a7a5880d3"
        },
        {
            "title": "DFINITY and Internet Computer Protocol Have Already Won",
            "content": "The article highlights the strong collaboration and mutual respect between Dominic Williams, founder of DFINITY, and Vitalik Buterin, co-founder of Ethereum, emphasizing DFINITY’s technical innovation and its role as a “sister network” to Ethereum. It suggests that recent developments and endorsements position the Internet Computer Protocol as a groundbreaking force in the blockchain ecosystem, potentially rivaling Ethereum.",
            "date": "December 21, 2024",
            "url": "https://medium.com/@iantdover/dfinity-and-internet-computer-protocol-have-already-won-ee800eba3807"
        },
        {
            "title": "Cloud Compute as a Public Good: A Case for Internet Computer Protocol",
            "content": "The Internet Computer Protocol (ICP) positions itself as a revolutionary blockchain platform that merges the performance of traditional cloud computing with the security and decentralization of Web3, offering unmatched computational efficiency and cost-effectiveness. By enabling decentralized applications, data storage, and alternatives to Big Tech solutions, ICP aims to disrupt industries such as cloud computing, AI, and gaming while promoting accessibility and sustainability.",
            "date": "December 19, 2024",
            "url": "https://medium.com/@iantdover/cloud-compute-as-a-public-good-a-case-for-internet-computer-protocol-5baa0d3ba8d8"
        },
        {
            "title": "The Reddit Comment that Got My Account Permanently Banned",
            "content": "After being permanently banned from Reddit for an innocuous comment about the Internet Computer Protocol (ICP), the author reflects on the implications of centralized platforms suppressing dissenting or innovative ideas. They advocate for decentralized platforms like OpenChat, which leverage democratic governance to protect free expression and ensure community-driven censorship decisions.",
            "date": "December 16, 2024",
            "url": "https://medium.com/@iantdover/the-reddit-comment-that-got-my-account-permanently-banned-778d9fd04e49"
        },
        {
            "title": "Causal Inference: Explaining Regression Discontinuity Design with Illustrations",
            "content": "A primer on regression discontinuity design.",
            "date": "December 4, 2024",
            "url": "https://medium.com/@iantdover/causal-inference-explaining-regression-discontinuity-design-with-illustrations-7427be30fd1d"
        },
        {
            "title": "Why a Multi-Chain Future Does Nothing to Prevent Wealth Inequality in Crypto",
            "content": "The article critiques the notion of a multi-chain future as a solution to wealth inequality in crypto, highlighting persistent disparities in wealth distribution (measured by the Gini coefficient) and decentralization (measured by the Nakamoto coefficient). It explores how even in multi-chain ecosystems, concentration of wealth and power remains a challenge, underscoring the need for more equitable frameworks within blockchain technology.",
            "date": "December 4, 2024",
            "url": "https://medium.com/@iantdover/why-a-multi-chain-future-does-nothing-to-prevent-wealth-inequality-in-crypto-a9b6ba96e8f2"
        },
        {
            "title": "Developer’s Perspective on Internet Computer Protocol (ICP)",
            "content": "The article explores the Internet Computer Protocol (ICP) as a decentralized alternative to traditional cloud providers, emphasizing its cost efficiency, scalability, and integrated tools for developers. It highlights ICP’s advantages, such as rapid transaction speeds, built-in routing layers, and reduced complexity for building decentralized applications, while also addressing current limitations like the need for enhanced secrets management and granular resource control.",
            "date": "November 29, 2024",
            "url": "https://medium.com/@iantdover/developers-perspective-on-internet-computer-protocol-icp-9ca1969c8993"
        },
    ]

    # Pagination variables
    page = request.args.get("page", 1, type=int)  # Get the page number from the query string
    per_page = 5  # Number of posts per page
    total_posts = len(blog_posts)
    total_pages = (total_posts + per_page - 1) // per_page  # Calculate total pages

    # Slice the posts for the current page
    start = (page - 1) * per_page
    end = start + per_page
    paginated_posts = blog_posts[start:end]

    return render_template("blog.html", posts=paginated_posts, page=page, total_pages=total_pages)

@app.route("/papers")
def papers():
    papers = [
        {
            "title": "Deep Convolutional Neural Network Ensemble for Improved Malaria Parasite Detection",
            "content": "Abstract—Malaria prognosis, performed through the identi-fication of parasites using microscopy, is a vital step in theearly initiation of treatment. Malaria inducing parasites suchas Plasmodium falciparum are difficult to identify and thus havea high mortality rate. For these reasons, a deep convolutionalneural network algorithm is proposed in this paper to aid inaccurately identifying parasitic cells from red blood smears. Byusing a mixture of machine learning techniques such as transferlearning, a cyclical and constant learning rate, and ensemblemethods, we have developed a model capable of accuratelyidentifying parasitic cells within red blood smears. 14 networkspretrained from the ImageNet database are retrained with thefully connected layers replaced. A cyclical and constant learningrate are used to traverse local minima in each network. Theoutput of each trained neural network is representing a singlevote that is used in the classification process. Majority votingcriteria are applied in the final classification decision betweenthe candidate malaria cells. Several experiments were conductedto evaluate the performance of the proposed model. The NIHMalaria Dataset from the National Institute of Health, a datasetof 27,558 images formed from microscopic patches of red bloodsmears, is used in these experiments. The dataset is segmentedinto 80% training set, 10% validation set, and 10% test set. Thevalidation set is used as the decision metric for choosing ensemblenetwork architectures and the test set is used as the evaluationmetric for each model. Different ensemble network architecturesare experimented with and promising performance is observedon the test dataset with the best models achieving a test accuracybetter than several state-of-the-art methodologies. ",
            "date": "October 2020",
            "url": "https://www.researchgate.net/publication/351487626_Deep_Convolutional_Neural_Network_Ensemble_for_Improved_Malaria_Parasite_Detection"
        },
        {
            "title": "FUSED DEEP CONVOLUTIONAL NEURAL NETWORK FOR PRECISION DIAGNOSIS OF COVID-19 USING CHEST X-RAY IMAGES A PREPRINT",
            "content": "With a Coronavirus disease (COVID-19) case count exceeding 10 million worldwide, there is an increased need for a diagnostic capability. The main variables in increasing diagnostic capability are reduced cost, turnaround or diagnosis time, and upfront equipment cost and accessibility. Two candidates for machine learning COVID-19 diagnosis are Computed Tomography (CT) scans and plain chest X-rays. While CT scans score higher in sensitivity, they have a higher cost, maintenance requirement, and turnaround time as compared to plain chest X-rays. The use of portable chest X-radiograph (CXR) is recommended by the American College of Radiology (ACR) since using CT places a massive burden on radiology services. Therefore, X-ray imagery paired with machine learning techniques is proposed a first-line triage tool for COVID-19 diagnostics. In this paper we propose a computer-aided diagnosis (CAD) to accurately classify chest X-ray scans of COVID-19 and normal subjects by fine-tuning several neural networks (ResNet18, ResNet50, DenseNet201) pre-trained on the ImageNet dataset. These neural networks are fused in a parallel architecture and the voting criteria are applied in the final classification decision between the candidate object classes where the output of each neural network is representing a single vote. Several experiments are conducted on the weakly labeled COVID-19-CT-CXR dataset consisting of 263 COVID-19 CXR images extracted from PubMed Central Open Access subsets combined with 25 normal classification CXR images. These experiments show an optimistic result and a capability of the proposed model to outperforming many state-of-the-art algorithms on several measures. Using k-fold cross-validation and a bagging classifier ensemble, we achieve an accuracy of 99.7% and a sensitivity of 100%.",
            "date": "November 2020",
            "url": "https://www.researchgate.net/publication/344324945_FUSED_DEEP_CONVOLUTIONAL_NEURAL_NETWORK_FOR_PRECISION_DIAGNOSIS_OF_COVID-19_USING_CHEST_X-RAY_IMAGES_A_PREPRINT"
        },
        {
            "title": "Data-Over-Sound Robot",
            "content": "Created a data-over-sound robot.",
            "date": "June 2020",
            "url": "https://www.researchgate.net/publication/341936244_Data-Over-Sound_Robot"
        },
    ]

    # Pagination variables
    page = request.args.get("page", 1, type=int)  # Get the page number from the query string
    per_page = 1  # Number of papers per page
    total_papers = len(papers)
    total_pages = (total_papers + per_page - 1) // per_page  # Calculate total pages

    # Slice the posts for the current page
    start = (page - 1) * per_page
    end = start + per_page
    paginated_papers = papers[start:end]

    return render_template("papers.html", posts=paginated_papers, page=page, total_pages=total_pages)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5003))
    app.run(debug=True, host="0.0.0.0", port=port)
