# Threat and opportunity examples

These four cases are the two highest-ranked firms for threat and the two highest-ranked for opportunity. They illustrate traceable connections, not an independent validation sample. Ranks include all 894 filings without processing flags and use minimum ranks for ties.

Hearing-name checks use documented aliases in the full saved hearing, including appendices. Matching ignores case and repeated whitespace and requires word boundaries. It is not exhaustive entity resolution. The industry baseline requires Facebook's modal NAICS3 (519), using the same historical reference mapping as the original figures.

Raw model labels are preserved, including questionable tags. Inspection here is not independent human validation.

<a id="0001558370-18-001043"></a>
## Total System Services

Threat rank 1/894; 21/87 threat sentences (24.14%); all recorded counts: threat 21, neutral 7, opportunity 0.

NAICS 522. Filed 2018-02-23; 45 days before hearing. [SEC filing](https://www.sec.gov/Archives/edgar/data/721683/000155837018001043/tss-20171231x10k.htm); [saved Item 1](<../../01 - Inputs/Source Filings/0001558370-18-001043_source.txt>).

Aliases searched and match counts: {'Total System Services': 0, 'TSYS': 0}.

Context, sentence 42: For example, in the United States, we and our financial institution clients are, respectively, subject to the Federal Trade Commission’s and the federal banking regulators’ privacy and information safeguarding requirements under the Gramm-Leach-Bliley Act.

**Selected sentence 48 / recorded label threat:** In many jurisdictions consumers must be notified in the event of a data breach, and such notification requirements continue to increase in scope and cost.

Interpretation: The sentence explicitly links breach notification to increasing scope and cost.

All model tags are retained below, including statements that may concern neighboring subjects or support a different directional interpretation. No counts or ranks are manually corrected.

### All retained tags

| Sentence | Recorded label | Original text |
|---:|---|---|
| 41 | neutral | Aspects of our business are also subject, directly or indirectly, to business and trade practices regulation in the United States, the European Union and elsewhere. |
| 42 | threat | For example, in the United States, we and our financial institution clients are, respectively, subject to the Federal Trade Commission’s and the federal banking regulators’ privacy and information safeguarding requirements under the Gramm-Leach-Bliley Act. |
| 43 | threat | These requirements limit the manner in which personal information may be collected, stored, used and disclosed. |
| 44 | threat | The Federal Trade Commission’s information safeguarding rules require us to develop, implement and maintain a written, comprehensive information security program containing safeguards that are appropriate for our size and complexity, the nature and scope of our activities and the sensitivity of any customer information at issue. |
| 45 | threat | Our financial institution clients in the United States are subject to similar requirements under the guidelines issued by the federal banking regulators. |
| 46 | threat | As part of their compliance with these requirements, each of our U.S. financial institution clients is expected to have a program in place for responding to unauthorized access to, or use of, customer information that could result in substantial harm or inconvenience to customers and they are also responsible for our compliance efforts as a major service provider. |
| 47 | threat | In addition, regulators are proposing new laws or regulations which could require us to adopt certain cybersecurity and data handling practices. |
| 48 | threat | In many jurisdictions consumers must be notified in the event of a data breach, and such notification requirements continue to increase in scope and cost. |
| 49 | threat | The changing privacy laws in the United States, Europe and elsewhere, including the adoption by the European Union of the General Data Protection Regulation, which will become effective in May 2018, create new individual privacy rights and impose increased obligations on companies handling personal data. |
| 50 | threat | Information concerning our cybersecurity risks and how a cybersecurity incident could materially affect our business is discussed under the caption “Security breaches of our systems, including as a result of cyber-attacks, may damage client relations, our reputation and expose us to financial liability” under “Risk Factors” in Part I, Item IA of this annual report. |
| 60 | threat | We and the rest of the financial services industry continue to experience increased legislative and regulatory scrutiny, including the enactment of additional legislative and regulatory initiatives such as the Dodd-Frank Wall Street Reform and Consumer Protection Act (“Reform Act”) in 2010. |
| 61 | threat | The Reform Act has resulted in significant structural and other changes to the regulation of the financial services industry. |
| 62 | threat | The Reform Act, among other things, provides for the regulation and oversight by the Board of Governors of the Federal Reserve System (“Board”) of debit interchange fees that are typically paid by acquirers and charged or received by a payment card network for the purpose of compensating an issuer for its involvement in an electronic debit transaction. |
| 63 | threat | In accordance with the Reform Act, the Board capped the maximum U.S. debit interchange fee assessed for debit cards issued by large financial institutions at twenty-one cents per transaction plus five basis points, before applying a fraud prevention adjustment of up to an additional one cent. |
| 64 | neutral | The cap on interchange fees has not had a significant negative impact on our business. |
| 65 | threat | The Reform Act also created a new Consumer Financial Protection Bureau (“CFPB”) with responsibility for regulating consumer financial products and services and enforcing most federal consumer protection laws in the area of financial services, including consumer credit and the prepaid card industry. |
| 66 | threat | For example, the CFPB has promulgated a new rule regarding prepaid financial products, which, among other things, will establish new disclosure requirements specific to prepaid accounts, eliminate certain fees that may currently be imposed on prepaid accounts, and make it economically unfeasible for a prepaid card provider such as our Netspend business to offer courtesy overdraft protection on prepaid accounts. |
| 67 | neutral | The rule is scheduled to become effective April 1, 2019. |
| 68 | threat | Similarly, other future actions of the CFPB may make payment card or product transactions generally less attractive to card issuers, acquirers, consumers and merchants by further regulatory disclosures, payment card practices, fees, routing and other matters with respect to credit, debit and prepaid cards, and thus negatively impact our business. |
| 72 | neutral | State Wage Payment Laws and Regulations. |
| 73 | threat | The use of payroll card programs as a means for an employer to remit wages or other compensation to its employees or independent contractors is governed by state labor laws related to wage payments, which laws are subject to change. |
| 74 | neutral | The paycard portion of our Netspend business includes payroll cards and convenience checks and is designed to allow employers to comply with applicable state wage and hour laws. |
| 75 | neutral | Most states permit the use of payroll cards as a method of paying wages to employees, either through statutory provisions allowing such use or, in the absence of specific statutory guidance, the adoption by state labor departments of formal or informal policies allowing for their use. |
| 76 | threat | Nearly every state allowing payroll cards places certain requirements and/or restrictions on their use as a wage payment method, the most common of which involve obtaining the prior written consent of the employee, limitations on fees and disclosure requirements. |
| 77 | neutral | Telephone Consumer Protection Act. |
| 78 | threat | We are subject to the Federal Telephone Consumer Protection Act and various state laws to the extent we place telephone calls and short message service (“SMS”) messages to clients and consumers. |
| 79 | threat | The Telephone Consumer Protection Act regulates certain telephone calls and SMS messages placed using automatic telephone dialing systems or artificial or prerecorded voices. |
| 80 | threat | We are subject to unclaimed or abandoned property laws in the United States and in foreign countries that require us to transfer to certain government authorities the unclaimed property of others that we hold when that property has been unclaimed for a certain period of time. |

### Complete input blocks and recorded responses

#### Block 0: sentences 1–40

```text
[1] Based in Columbus, Georgia, and traded on the New York Stock Exchange under the symbol “TSS,” we are a global payment solutions provider that provides payment processing services, merchant services and related payment services to financial and nonfinancial institutions.
[2] In addition, we provide general purpose reloadable (“GPR”) prepaid and payroll cards, demand deposit accounts and other financial service solutions to the underbanked and other consumers and businesses.
[3] The services we provide are divided into three operating segments, Merchant Solutions, which accounted for 49% of our revenues in 2017, Issuer Solutions, which accounted for 36% of our revenues in 2017 and Netspend, which accounted for 15% of our revenues in 2017.
[4] Due to the somewhat seasonal nature of the credit card industry, our revenues and results of operations have generally increased in the fourth quarter of each year because of increased transaction and authorization volumes during the traditional holiday shopping season.
[5] Our intellectual property portfolio is a component of our ability to be a leading provider of transaction processing and other payment-related services.
[6] We diligently protect and work to build our intellectual property rights through patent, servicemark and trade secret laws.
[7] We also use various licensed intellectual property to conduct our business.
[8] In addition to using our intellectual property in our own operations, we grant licenses to certain of our clients to use our intellectual property.
[9] A significant amount of our revenues is derived from long-term contracts with large clients.
[10] The loss of one of our large clients could have a material adverse effect on our financial position, results of operations and cash flows.
[11] See “Major Customer” and “Operating Segments” under the “Financial Review” Section on pages 17 through 21, and Note 20 on pages 72 through 74 of the Annual Report which are incorporated in this document by reference.
[12] Each of our three business segments encounters vigorous competition in connection with the services it provides.
[13] Our Issuer Solutions segment encounters competition from credit card processing firms, third-party card processing software vendors and various other firms that provide products and services to credit card issuers in the United States and internationally.
[14] The United States market for third party processing for credit card issuers is primarily serviced by three vendors, including TSYS, with our largest competitor being a subsidiary of First Data Corporation.
[15] We believe that as of December 31, 2017, we are the largest third party processor for credit card issuers in North America and one of the largest in Europe based on net revenues derived from solutions for credit card issuers.
[16] Further, we believe that during 2017 we provided issuer processing services for approximately 40% of the domestic Visa and Mastercard credit card accounts issued in the United States, approximately 80% issued in Canada and approximately 20% issued in TSYS’ Home European Markets (UK, Netherlands, Italy, Germany and Switzerland).
[17] The principal methods of competition between us and our competitors are system performance and reliability, servicing capability, breadth of features and functionality, disaster recovery capabilities and business continuity preparedness, data security, scalability and flexibility of infrastructure and price.
[18] Our Merchant Solutions segment competes with financial institutions and merchant acquirers who provide businesses with merchant services and related services.
[19] Our primary competitors include First Data Corporation (and its alliances), Worldpay, Inc., Global Payments Inc. and Elavon, Inc.
[20] Additionally, payment networks such as Visa and Mastercard are increasingly offering products and services that compete with our products and services.
[21] We also provide third party processing and related services to merchant acquirers, Independent Sales Organizations (“ISOs”) and financial institutions.
[22] We believe that as of December 31, 2017, we are the sixth largest merchant acquirer in the United States based on net revenue and one of the top two providers of third party processing services.
[23] The principal methods of competition between us and our competitors include quality of distribution partners, breadth of features and functionality, service levels, system performance and reliability, data security and price.
[24] Our Netspend segment primarily competes with other prepaid program managers to provide the underbanked and other consumers and businesses with financial service solutions.
[25] Our primary competitors in this space include Green Dot Corporation, InComm and First Data Corporation.
[26] As of December 31, 2017, we believe that we are the largest prepaid program manager in the United States based on gross dollar volume (total spending on the accounts we manage) processed during 2017.
[27] The principal methods of competition between us and our competitors include diversity and strength of distribution, breadth and strength of innovative features and functionality, quality of service, reliability of system performance and security and price.
[28] Government regulation affects key aspects of our business, in the U.S. as well as internationally.
[29] In addition, we are registered with Visa, Mastercard, American Express and the Discover Network as a service provider and are subject to their respective rules which subject us to a variety of fines or penalties that may be levied by the card networks for certain acts or omissions.
[30] Set forth below is a brief summary of some of the significant laws and regulations that apply to us.
[31] These descriptions are not exhaustive and are qualified in their entirety by reference to the particular statutory or regulatory provision, which provisions are subject to change.
[32] Because we provide electronic payment processing services to banks and other financial institutions, we are subject to examination by the Federal Financial Institutions Examination Council (“FFIEC”), an interagency body comprised primarily of federal banking regulators, and also subject to examination by the various state financial regulatory agencies which supervise and regulate the financial institutions for which we provide electronic payment processing and other payment related services.
[33] The FFIEC examines large data processors in order to identify and mitigate risks associated with systemically significant service providers, including specifically the risks they may pose to the banking industry.
[34] Money Transmitter and Payment Instrument Laws and Regulations.
[35] Our Netspend business is subject to money transfer and payment instrument licensing regulations.
[36] We have obtained licenses to operate as a money transmitter in 48 states and the District of Columbia.
[37] The remaining U.S. jurisdictions either do not currently regulate money transmitters or have rendered a regulatory determination or a legal interpretation that the money services laws of that jurisdiction do not require us to obtain a license in connection with the conduct of our business.
[38] In those states where we are licensed as a money transmitter, our Netspend business is subject to direct supervision and regulation by the relevant state banking departments or similar agencies charged with enforcement of the money transmitter statutes and we must comply with various requirements, such as those related to the maintenance of a certain level of net worth, surety bonding, selection and oversight of our authorized agents, maintaining permissible investments in an amount equal to our outstanding payment obligations, recordkeeping and reporting and disclosures to consumers.
[39] Our Netspend business is also subject to periodic examinations by the relevant licensing authorities, which may include reviews of our compliance practices, policies and procedures, financial position and related records, various agreements that we have with our issuing banks, distributors and other third parties, privacy and data security policies and procedures and other matters related to our business.
[40] Privacy, Information Security, and Other Business Practices Regulation.
```

Gate response:

```text
[69]
```

#### Block 1: sentences 41–80

```text
[41] Aspects of our business are also subject, directly or indirectly, to business and trade practices regulation in the United States, the European Union and elsewhere.
[42] For example, in the United States, we and our financial institution clients are, respectively, subject to the Federal Trade Commission’s and the federal banking regulators’ privacy and information safeguarding requirements under the Gramm-Leach-Bliley Act.
[43] These requirements limit the manner in which personal information may be collected, stored, used and disclosed.
[44] The Federal Trade Commission’s information safeguarding rules require us to develop, implement and maintain a written, comprehensive information security program containing safeguards that are appropriate for our size and complexity, the nature and scope of our activities and the sensitivity of any customer information at issue.
[45] Our financial institution clients in the United States are subject to similar requirements under the guidelines issued by the federal banking regulators.
[46] As part of their compliance with these requirements, each of our U.S. financial institution clients is expected to have a program in place for responding to unauthorized access to, or use of, customer information that could result in substantial harm or inconvenience to customers and they are also responsible for our compliance efforts as a major service provider.
[47] In addition, regulators are proposing new laws or regulations which could require us to adopt certain cybersecurity and data handling practices.
[48] In many jurisdictions consumers must be notified in the event of a data breach, and such notification requirements continue to increase in scope and cost.
[49] The changing privacy laws in the United States, Europe and elsewhere, including the adoption by the European Union of the General Data Protection Regulation, which will become effective in May 2018, create new individual privacy rights and impose increased obligations on companies handling personal data.
[50] Information concerning our cybersecurity risks and how a cybersecurity incident could materially affect our business is discussed under the caption “Security breaches of our systems, including as a result of cyber-attacks, may damage client relations, our reputation and expose us to financial liability” under “Risk Factors” in Part I, Item IA of this annual report.
[51] Anti-money Laundering and Counter Terrorist Regulation.
[52] The Financial Crimes Enforcement Network of the U.S. Department of the Treasury (“FinCEN”) has issued a rule regarding the applicability of the Bank Secrecy Act's anti-money laundering provisions to “prepaid access programs.”
[53] This rulemaking clarifies the anti-money laundering obligations for entities, such as our Netspend business and its distributors, engaged in the provision and sale of prepaid access devices like our GPR prepaid cards.
[54] Our Netspend business has registered with FinCEN as a money services business.
[55] This registration results in our having direct responsibility to maintain and implement an anti-money laundering compliance program.
[56] We are subject to anti-corruption laws and regulations, including the U.S. Foreign Corrupt Practices Act, the UK Bribery Act and other laws that generally prohibit the making or offering of improper payments to foreign government officials and political figures for the purpose of obtaining or retaining business or to gain an unfair business advantage.
[57] In addition, as are all U.S. persons, we are also subject to regulations imposed by the U.S. Department of the Treasury Office of Foreign Assets Control (“OFAC”) which prohibit or restrict financial and other transactions with specified countries and designated individuals and entities such as terrorists and narcotics traffickers.
[58] We have procedures and controls in place which are designed to protect against having direct business dealings with such prohibited countries, individuals or entities.
[59] We also have procedures and controls in place which are designed to allow our processing clients to protect against having direct business dealings with such prohibited countries, individuals or entities.
[60] We and the rest of the financial services industry continue to experience increased legislative and regulatory scrutiny, including the enactment of additional legislative and regulatory initiatives such as the Dodd-Frank Wall Street Reform and Consumer Protection Act (“Reform Act”) in 2010.
[61] The Reform Act has resulted in significant structural and other changes to the regulation of the financial services industry.
[62] The Reform Act, among other things, provides for the regulation and oversight by the Board of Governors of the Federal Reserve System (“Board”) of debit interchange fees that are typically paid by acquirers and charged or received by a payment card network for the purpose of compensating an issuer for its involvement in an electronic debit transaction.
[63] In accordance with the Reform Act, the Board capped the maximum U.S. debit interchange fee assessed for debit cards issued by large financial institutions at twenty-one cents per transaction plus five basis points, before applying a fraud prevention adjustment of up to an additional one cent.
[64] The cap on interchange fees has not had a significant negative impact on our business.
[65] The Reform Act also created a new Consumer Financial Protection Bureau (“CFPB”) with responsibility for regulating consumer financial products and services and enforcing most federal consumer protection laws in the area of financial services, including consumer credit and the prepaid card industry.
[66] For example, the CFPB has promulgated a new rule regarding prepaid financial products, which, among other things, will establish new disclosure requirements specific to prepaid accounts, eliminate certain fees that may currently be imposed on prepaid accounts, and make it economically unfeasible for a prepaid card provider such as our Netspend business to offer courtesy overdraft protection on prepaid accounts.
[67] The rule is scheduled to become effective April 1, 2019.
[68] Similarly, other future actions of the CFPB may make payment card or product transactions generally less attractive to card issuers, acquirers, consumers and merchants by further regulatory disclosures, payment card practices, fees, routing and other matters with respect to credit, debit and prepaid cards, and thus negatively impact our business.
[69] In addition, the Reform Act created a Financial Stability Oversight Council that has the authority to determine whether nonbank financial companies such as TSYS should be supervised by the Board because they are systemically important to the U.S. financial system.
[70] To date, the Financial Stability Oversight Council does not appear to be focused on regulating entities such as TSYS.
[71] However, any such future designation would result in increased regulatory burdens on our business.
[72] State Wage Payment Laws and Regulations.
[73] The use of payroll card programs as a means for an employer to remit wages or other compensation to its employees or independent contractors is governed by state labor laws related to wage payments, which laws are subject to change.
[74] The paycard portion of our Netspend business includes payroll cards and convenience checks and is designed to allow employers to comply with applicable state wage and hour laws.
[75] Most states permit the use of payroll cards as a method of paying wages to employees, either through statutory provisions allowing such use or, in the absence of specific statutory guidance, the adoption by state labor departments of formal or informal policies allowing for their use.
[76] Nearly every state allowing payroll cards places certain requirements and/or restrictions on their use as a wage payment method, the most common of which involve obtaining the prior written consent of the employee, limitations on fees and disclosure requirements.
[77] Telephone Consumer Protection Act.
[78] We are subject to the Federal Telephone Consumer Protection Act and various state laws to the extent we place telephone calls and short message service (“SMS”) messages to clients and consumers.
[79] The Telephone Consumer Protection Act regulates certain telephone calls and SMS messages placed using automatic telephone dialing systems or artificial or prerecorded voices.
[80] We are subject to unclaimed or abandoned property laws in the United States and in foreign countries that require us to transfer to certain government authorities the unclaimed property of others that we hold when that property has been unclaimed for a certain period of time.
```

Gate response:

```text
[65, 68, 93]
```

Confirm response:

```text
[[41, 68, "N"], [42, 68, "T"], [43, 68, "T"], [44, 68, "T"], [45, 68, "T"], [46, 68, "T"], [47, 68, "T"], [48, 68, "T"], [49, 68, "T"], [50, 68, "T"], [60, 68, "T"], [61, 68, "T"], [62, 68, "T"], [63, 68, "T"], [64, 68, "N"], [65, 68, "T"], [66, 68, "T"], [67, 68, "N"], [68, 68, "T"], [72, 68, "N"], [73, 68, "T"], [74, 68, "N"], [75, 68, "N"], [76, 68, "T"], [77, 68, "N"], [78, 68, "T"], [79, 68, "T"], [80, 68, "T"]]
```

#### Block 2: sentences 81–87

```text
[81] Moreover, we are subject to audit by state regulatory authorities with regard to our escheatment practices.
[82] Our website address is www.tsys.com.
[83] You may obtain free electronic copies of our Annual Reports on Form 10-K, Quarterly Reports on Form 10-Q, Current Reports on Form 8-K, and all amendments to those reports in the Investor Relations section of our website under the heading “SEC Filings.”
[84] These reports are available on our website as soon as reasonably practicable after we electronically file them with the Securities and Exchange Commission.
[85] We have adopted a Code of Business Conduct and Ethics for our directors, officers and employees and have also adopted Corporate Governance Guidelines.
[86] Our Code of Business Conduct and Ethics, Corporate Governance Guidelines and the charters of our board committees are available in the Corporate Governance section of our website at www.tsys.com under “Investor Relations” then “Corporate Governance.”
[87] For more information about our business see the “Financial Overview” Section on pages 12 and 13, the “Financial Review” Section on pages 14 through 32 and Note 1, Note 7, Note 14, Note 20, Note 22 and Note 25 of Notes to Consolidated Financial Statements on pages 38 through 51, pages 54 and 55, pages 63 through 65, pages 72 through 74, pages 74 through 76, and pages 77 and 78 of the Annual Report which are incorporated in this document by reference.
```

Gate response:

```text
[]
```

<a id="0001326801-18-000009"></a>
## Facebook

Threat rank 2/894; 15/78 threat sentences (19.23%); all recorded counts: threat 15, neutral 0, opportunity 0.

NAICS 519. Filed 2018-02-01; 67 days before hearing. [SEC filing](https://www.sec.gov/Archives/edgar/data/1326801/000132680118000009/fb-12312017x10k.htm); [saved Item 1](<../../01 - Inputs/Source Filings/0001326801-18-000009_source.txt>).

Aliases searched and match counts: {'Facebook': 4464}.

Context, sentence 54: In addition, the new European General Data Protection Regulation (GDPR) will take effect in May 2018 and will apply to all of our products and services that provide service in Europe.

**Selected sentence 55 / recorded label threat:** The GDPR will include operational requirements for companies that receive or process personal data of residents of the European Union that are different than those currently in place in the European Union, and will include significant penalties for non- compliance.

Interpretation: The sentence identifies operational requirements and penalties for noncompliance.

All model tags are retained below, including statements that may concern neighboring subjects or support a different directional interpretation. No counts or ranks are manually corrected.

### All retained tags

| Sentence | Recorded label | Original text |
|---:|---|---|
| 45 | threat | We are subject to a number of U.S. federal and state and foreign laws and regulations that affect companies conducting business on the Internet. |
| 46 | threat | Many of these laws and regulations are still evolving and being tested in courts, and could be interpreted in ways that could harm our business. |
| 47 | threat | These may involve user privacy, data protection and personal information, rights of publicity, content, intellectual property, advertising, marketing, distribution, data security, data retention and deletion, electronic contracts and other communications, competition, protection of minors, consumer protection, telecommunications, product liability, taxation, economic or other trade prohibitions or sanctions, securities law compliance, and online payment services. |
| 48 | threat | In particular, we are subject to federal, state, and foreign laws regarding privacy and protection of people's data. |
| 49 | threat | Foreign data protection, privacy, content, competition, and other laws and regulations can be more restrictive than those in the United States. |
| 50 | threat | U.S. federal and state and foreign laws and regulations, which in some cases can be enforced by private parties in addition to government entities, are constantly evolving and can be subject to significant change. |
| 51 | threat | As a result, the application, interpretation, and enforcement of these laws and regulations are often uncertain, particularly in the new and rapidly evolving industry in which we operate, and may be interpreted and applied inconsistently from country to country and inconsistently with our current policies and practices. |
| 52 | threat | Proposed or new legislation and regulations could also significantly affect our business. |
| 53 | threat | There currently are a number of proposals pending before federal, state, and foreign legislative and regulatory bodies. |
| 54 | threat | In addition, the new European General Data Protection Regulation (GDPR) will take effect in May 2018 and will apply to all of our products and services that provide service in Europe. |
| 55 | threat | The GDPR will include operational requirements for companies that receive or process personal data of residents of the European Union that are different than those currently in place in the European Union, and will include significant penalties for non- compliance. |
| 56 | threat | Similarly, there are a number of legislative proposals in the United States, at both the federal and state level, that could impose new obligations in areas affecting our business, such as liability for copyright infringement by third parties. |
| 57 | threat | In addition, some countries are considering or have passed legislation implementing data protection requirements or requiring local storage and processing of data or similar requirements that could increase the cost and complexity of delivering our services. |
| 58 | threat | We are currently, and may in the future be, subject to regulatory orders or consent decrees. |
| 59 | threat | Violation of existing or future regulatory orders or consent decrees could subject us to substantial monetary fines and other penalties that could negatively affect our financial condition and results of operations. |

### Complete input blocks and recorded responses

#### Block 0: sentences 1–40

```text
[1] Our mission is to give people the power to build community and bring the world closer together.
[2] Our top priority is to build useful and engaging products that enable people to connect and share with friends and family through mobile devices, personal computers, and other surfaces.
[3] We also help people discover and learn about what is going on in the world around them, enable people to share their opinions, ideas, photos and videos, and other activities with audiences ranging from their closest friends to the public at large, and stay connected everywhere by accessing our products, including:
[4] Facebook enables people to connect, share, discover, and communicate with each other on mobile devices and personal computers.
[5] There are a number of different ways to engage with people on Facebook, the most important of which is News Feed which displays an algorithmically-ranked series of stories and advertisements individualized for each person.
[6] Instagram is a community for sharing visual stories through photos, videos, and direct messages.
[7] Instagram is also a place for people to stay connected with the interests and communities that they care about.
[8] Messenger is a messaging application that makes it easy for people to connect with other people, groups and businesses across a variety of platforms and devices.
[9] WhatsApp is a fast, simple, and reliable messaging application that is used by people around the world to connect securely and privately.
[10] Our Oculus virtual reality technology and content platform power products that allow people to enter a completely immersive and interactive environment to train, learn, play games, consume content, and connect with others.
[11] We generate substantially all of our revenue from selling advertising placements to marketers.
[12] Our ads enable marketers to reach people based on a variety of factors including age, gender, location, interests, and behaviors.
[13] Marketers purchase ads that can appear in multiple places including on Facebook, Instagram, Messenger, and third-party applications and websites.
[14] We are also investing in a number of longer-term initiatives, such as connectivity efforts, artificial intelligence research, and augmented and virtual reality, to develop technologies that we believe will help us better serve our communities and pursue our mission to give people the power to build community and bring the world closer together.
[15] Our business is characterized by innovation, rapid change, and disruptive technologies.
[16] We compete with companies that sell advertising, as well as with companies that provide social, media, and communication products and services that are designed to engage users on mobile devices and online.
[17] We face significant competition in every aspect of our business, including from companies that facilitate communication and the sharing of content and information, companies that enable marketers to display advertising, companies that distribute video and other forms of media content, and companies that provide development platforms for applications developers.
[18] We compete to attract, engage, and retain people who use our products, to attract and retain marketers, and to attract and retain developers to build compelling mobile and web applications that integrate with our products.
[19] We also compete with the following:
[20] Companies that offer products across broad platforms that replicate capabilities we provide.
[21] For example, Google has integrated social functionality into a number of its products, including search, video, and Android.
[22] Companies that develop applications, particularly mobile applications, that provide social or other communications functionality, such as messaging, photo- and video-sharing, and micro-blogging.
[23] Companies that provide regional social networks that have strong positions in particular countries.
[24] Traditional, online, and mobile businesses that provide media for marketers to reach their audiences and/or develop tools and systems for managing and optimizing advertising campaigns.
[25] Companies that develop and deliver virtual reality products and services.
[26] As we introduce or acquire new products, as our existing products evolve, or as other companies introduce new products and services, we may become subject to additional competition.
[27] Our product development philosophy is centered on continuous innovation in creating and improving products that are social by design, which means that our products are designed to place people and their social interactions at the core of the product experience.
[28] As our user base grows, and the level of engagement from the people who use our products continues to increase, including with video, our computing needs continue to expand.
[29] We make significant investments in technology both to improve our existing products and services and to develop new ones, as well as for our marketers and developers.
[30] We are also investing in protecting the security and integrity of our platform by investing in both people and technology to strengthen our systems against abuse.
[31] Our technology investments included research and development expenses of $7.75 billion , $5.92 billion and $4.82 billion in 2017, 2016 and 2015, respectively.
[32] For information about our research and development expenses, see Part II, Item 7, "Management's Discussion and Analysis of Financial Condition and Results of Operations—Results of Operations—Research and development" of this Annual Report on Form 10-K.
[33] The majority of our marketers use our self-service ad platform to launch and manage their advertising campaigns.
[34] We also have a global sales force that is focused on attracting and retaining advertisers and providing support to them throughout the stages of the marketing cycle from pre-purchase decision-making to real-time optimizations to post-campaign analytics.
[35] We work directly with these advertisers, through traditional advertising agencies, and with an ecosystem of specialized agencies and partners.
[36] We currently operate six support offices and more than 40 sales offices around the globe.
[37] We also invest in and rely on self-service tools to provide direct customer support to our users and partners.
[38] To date, our communities have grown organically with people inviting their friends to connect with them, supported by internal efforts to stimulate awareness and interest.
[39] In addition, we have invested and will continue to invest in marketing our products and services to build our brand, grow our user base, and increase engagement around the world.
[40] We leverage the utility of our products and our social distribution channels as our most effective marketing tools.
```

Gate response:

```text
[93, 94, 61, 65, 68, 69, 92]
```

Confirm response:

```text
[]
```

#### Block 1: sentences 41–78

```text
[41] To establish and protect our proprietary rights, we rely on a combination of patents, trademarks, copyrights, trade secrets, including know-how, license agreements, confidentiality procedures, non-disclosure agreements with third parties, employee disclosure and invention assignment agreements, and other contractual rights.
[42] In addition, to further protect our proprietary rights, from time to time we have purchased patents and patent applications from third parties.
[43] We do not believe that our proprietary technology is dependent on any single patent or copyright or groups of related patents or copyrights.
[44] We believe the duration of our patents is adequate relative to the expected lives of our products.
[45] We are subject to a number of U.S. federal and state and foreign laws and regulations that affect companies conducting business on the Internet.
[46] Many of these laws and regulations are still evolving and being tested in courts, and could be interpreted in ways that could harm our business.
[47] These may involve user privacy, data protection and personal information, rights of publicity, content, intellectual property, advertising, marketing, distribution, data security, data retention and deletion, electronic contracts and other communications, competition, protection of minors, consumer protection, telecommunications, product liability, taxation, economic or other trade prohibitions or sanctions, securities law compliance, and online payment services.
[48] In particular, we are subject to federal, state, and foreign laws regarding privacy and protection of people's data.
[49] Foreign data protection, privacy, content, competition, and other laws and regulations can be more restrictive than those in the United States.
[50] U.S. federal and state and foreign laws and regulations, which in some cases can be enforced by private parties in addition to government entities, are constantly evolving and can be subject to significant change.
[51] As a result, the application, interpretation, and enforcement of these laws and regulations are often uncertain, particularly in the new and rapidly evolving industry in which we operate, and may be interpreted and applied inconsistently from country to country and inconsistently with our current policies and practices.
[52] Proposed or new legislation and regulations could also significantly affect our business.
[53] There currently are a number of proposals pending before federal, state, and foreign legislative and regulatory bodies.
[54] In addition, the new European General Data Protection Regulation (GDPR) will take effect in May 2018 and will apply to all of our products and services that provide service in Europe.
[55] The GDPR will include operational requirements for companies that receive or process personal data of residents of the European Union that are different than those currently in place in the European Union, and will include significant penalties for non- compliance.
[56] Similarly, there are a number of legislative proposals in the United States, at both the federal and state level, that could impose new obligations in areas affecting our business, such as liability for copyright infringement by third parties.
[57] In addition, some countries are considering or have passed legislation implementing data protection requirements or requiring local storage and processing of data or similar requirements that could increase the cost and complexity of delivering our services.
[58] We are currently, and may in the future be, subject to regulatory orders or consent decrees.
[59] Violation of existing or future regulatory orders or consent decrees could subject us to substantial monetary fines and other penalties that could negatively affect our financial condition and results of operations.
[60] Various laws and regulations in the United States and abroad, such as the U.S. Bank Secrecy Act, the Dodd-Frank Act, the USA PATRIOT Act, and the Credit CARD Act, impose certain anti-money laundering requirements on companies that are financial institutions or that provide financial products and services.
[61] Under these laws and regulations, financial institutions are broadly defined to include money services businesses such as money transmitters, check cashers, and sellers or issuers of stored value or prepaid access products.
[62] Requirements imposed on financial institutions under these laws include customer identification and verification programs, record retention policies and procedures, and transaction reporting.
[63] To increase flexibility in how our online payments infrastructure (Payments) may evolve and to mitigate regulatory uncertainty, we have received certain money transmitter licenses in the United States and an Electronic Money (E-Money) license that allows us to conduct certain regulated payment activities in the participating member countries of the European Economic Area, which will generally require us to demonstrate compliance with many domestic and foreign laws relating to money transmission, gift cards and other prepaid access instruments, electronic funds transfers, anti-money laundering, charitable fundraising, counter-terrorist financing, gambling, banking and lending, financial privacy and data security, and import and export restrictions.
[64] We were incorporated in Delaware in July 2004.
[65] We completed our initial public offering in May 2012 and our Class A common stock is listed on The Nasdaq Global Select Market under the symbol "FB."
[66] Our principal executive offices are located at 1601 Willow Road, Menlo Park, California 94025, and our telephone number is (650) 543-4800.
[67] Facebook, the Facebook logo, FB, the Like button, Instagram, Oculus, WhatsApp, and our other registered or common law trademarks, service marks, or trade names appearing in this Annual Report on Form 10-K are the property of Facebook, Inc. or its affiliates.
[68] Other trademarks, service marks, or trade names appearing in this Annual Report on Form 10-K are the property of their respective owners.
[69] Information about Segment and Geographic Revenue
[70] Information about segment and geographic revenue is set forth in Notes 1 and 13 of our Notes to Consolidated Financial Statements included in Part II, Item 8, "Financial Statements and Supplementary Data" of this Annual Report on Form 10-K.
[71] Our website address is www.facebook.com.
[72] Our Annual Report on Form 10-K, Quarterly Reports on Form 10-Q, Current Reports on Form 8-K, and amendments to reports filed pursuant to Sections 13(a) and 15(d) of the Securities Exchange Act of 1934, as amended (Exchange Act), are filed with the U.S. Securities and Exchange Commission (SEC).
[73] We are subject to the informational requirements of the Exchange Act and file or furnish reports, proxy statements, and other information with the SEC.
[74] Such reports and other information filed by us with the SEC are available free of charge on our website at investor.fb.com when such reports are available on the SEC's website.
[75] We use our investor.fb.com and newsroom.fb.com websites as well as Mark Zuckerberg's Facebook Page (https://www.facebook.com/zuck) as means of disclosing material non-public information and for complying with our disclosure obligations under Regulation FD.
[76] The public may read and copy any materials filed by Facebook with the SEC at the SEC's Public Reference Room at 100 F Street, NE, Room 1580, Washington, DC 20549.
[77] The contents of the websites referred to above are not incorporated into this filing.
[78] Further, our references to the URLs for these websites are intended to be inactive textual references only.
```

Gate response:

```text
[47, 48, 49, 52, 54, 61, 65, 68, 69, 93, 92]
```

Confirm response:

```text
[[45, 68, "T"], [46, 68, "T"], [47, 68, "T"], [48, 68, "T"], [49, 68, "T"], [50, 68, "T"], [51, 68, "T"], [52, 68, "T"], [53, 68, "T"], [54, 68, "T"], [55, 68, "T"], [56, 68, "T"], [57, 68, "T"], [58, 68, "T"], [59, 68, "T"]]
```

<a id="0001564590-18-002088"></a>
## Paycom Software

Opportunity rank 1/894; 8/300 opportunity sentences (2.67%); all recorded counts: threat 5, neutral 0, opportunity 8.

NAICS 518. Filed 2018-02-14; 54 days before hearing. [SEC filing](https://www.sec.gov/Archives/edgar/data/1590955/000156459018002088/payc-10k_20171231.htm); [saved Item 1](<../../01 - Inputs/Source Filings/0001564590-18-002088_source.txt>).

Aliases searched and match counts: {'Paycom': 0}.

Context, sentence 259: Data privacy has become a significant issue in the United States and in other countries.

**Selected sentence 263 / recorded label opportunity:** We voluntarily obtain third-party security examinations relating to security and data privacy in accordance with Statement on Standards for Attestation Engagements (“SSAE”), No. 16, Reporting on Controls at a Service Organization.

Interpretation: Security assurance is explicit; growth, demand, or competitive advantage is not. The opportunity label requires review.

All model tags are retained below, including statements that may concern neighboring subjects or support a different directional interpretation. No counts or ranks are manually corrected.

### All retained tags

| Sentence | Recorded label | Original text |
|---:|---|---|
| 258 | threat | These regulations and laws cover, among others, information privacy. |
| 259 | threat | Data privacy has become a significant issue in the United States and in other countries. |
| 260 | threat | The regulatory framework for privacy issues worldwide is rapidly evolving and is likely to remain uncertain for the foreseeable future. |
| 261 | threat | Many federal, state and foreign government bodies and agencies have adopted or are considering adopting laws and regulations affecting or regarding the collection, use and disclosure of personal information. |
| 262 | threat | In the United States, these include, for example, rules and regulations promulgated under the authority of the Federal Trade Commission, the Health Insurance Portability and Accountability Act of 1996, the Family Medical Leave Act of 1993, the ACA and state breach notification laws. |
| 263 | opportunity | We voluntarily obtain third-party security examinations relating to security and data privacy in accordance with Statement on Standards for Attestation Engagements (“SSAE”), No. 16, Reporting on Controls at a Service Organization. |
| 264 | opportunity | Our SSAE examination is conducted every six months by one of the four largest independent international auditing firms, and addresses, among other areas, our physical and environmental safeguards for production data centers, data availability and integrity procedures, change management procedures and logical security procedures. |
| 265 | opportunity | In October 2016, we renewed a certification based on ISO/IEC 27001:2013 criteria, a security standard for Information Security Management Systems published by ISO covering our production, quality assurance and implementation environments. |
| 266 | opportunity | This independent assessment of our conformity to the ISO 27001 standard includes assessing security risks, designing and implementing comprehensive security controls and adopting an information security management process to meet security needs on an ongoing basis. |
| 267 | opportunity | The certification is valid until December 2019, with continuing assessments taking place annually. |
| 268 | opportunity | In April 2017, we renewed a certification based on ISO 9001:2008 criteria, a standard for the implementation of quality management processes published by ISO, covering our activities required to create and deliver our solution. |
| 269 | opportunity | This independent assessment of our conformity to the ISO 9001:2008 standard includes assessing the design and implementation of quality objectives to meet delivery standards on an ongoing basis. |
| 270 | opportunity | The certification is valid until September 2018, with continuing assessments taking place annually. |

### Complete input blocks and recorded responses

#### Block 0: sentences 1–40

```text
[1] Unless we state otherwise or the context otherwise requires, the terms “Paycom,” “we,” “us,” “our” and the “Company” refer to Paycom Software, Inc., a Delaware corporation, and its consolidated subsidiaries.
[2] We are a leading provider of a comprehensive, cloud-based HCM software solution delivered as SaaS.
[3] We provide functionality and data analytics that businesses need to manage the complete employment life cycle from recruitment to retirement.
[4] Our solution requires virtually no customization and is based on a core system of record maintained in a single database for all HCM functions, including talent acquisition, time and labor management, payroll, talent management and human resources (“HR”) management applications.
[5] Our user-friendly software allows for easy adoption of our solution by employees, enabling self-management of their HCM activities in the cloud, which reduces the administrative burden on employers and increases employee productivity.
[6] Organizations need sophisticated, flexible and intuitive applications that can quickly adapt to their evolving HCM requirements, streamline their HR processes and systems and enable them to control costs.
[7] We believe that the HCM needs of most organizations are currently served either by multiple providers in an attempt to replicate a comprehensive SaaS product or, to a lesser extent, by legacy providers offering outdated on-premise products.
[8] These approaches often result in challenges with system integration and data integrity, low scalability, high costs, extended delivery times and large up-front capital requirements.
[9] Because our solution was developed in-house and is based on a single platform, there is no need to integrate, update or access multiple databases, which are common issues with competitor offerings that use multiple third-party systems in order to link together their HCM offerings.
[10] Additionally, our solution maintains data integrity for accurate, actionable and real-time analytics and business intelligence and helps clients minimize the risk of compliance errors due to inaccurate or missing information.
[11] We deliver feature-rich applications while maintaining excellence in information security and quality management standards as evidenced by our International Organization for Standardization (“ISO”) certifications.
[12] We sell our solution directly through our internally trained, client-focused and highly skilled sales force based in offices across the United States.
[13] As a part of our client retention effort, a specialist within a dedicated team is assigned to each client to provide industry-leading, personalized service.
[14] We have over 20,000 clients, none of which constituted more than one-half of one percent of our revenues for the year ended December 31, 2017.
[15] We believe that as a result of our focus on client retention, we enjoy high client satisfaction as evidenced by an annual revenue retention rate of 91% from existing clients for each of the three years ended December 31, 2017, 2016 and 2015.
[16] We believe our revenue retention rate understates our client loyalty because this rate also includes former clients that were acquired or otherwise ceased operations.
[17] Since our founding, we have focused on providing an innovative SaaS HCM solution.
[18] As of December 31, 2017, we had 2,548 employees across the United States.
[19] For the years ended December 31, 2017, 2016 and 2015, our revenues were $433.0 million, $329.1 million and $224.7 million, respectively, representing year-over-year growth in revenues of approximately 32% and 4 7%, respectively.
[20] We currently derive the majority of our revenues from payroll processing.
[21] We are able to determine revenues from payroll processing because all of our clients are required to utilize our payroll application in order to access our other ap plications.
[22] We generally do not separately track our revenues across our other applications because we often sell applications in various groupings and configurations for a single price.
[23] We realized net income of $66.8 million, $43.8 million and $20.9 mill ion for the years ended December 31, 2017, 2016 and 2015, respectively.
[24] We offer an end-to-end SaaS HCM solution that provides our clients and their employees with immediate access to accurate and secure information and analytics at any time from any location where internet is available.
[25] We believe that our solution delivers the following benefits:
[26] Our solution offers functionality that manages the entire employment life cycle for employers and employees, from recruitment to retirement.
[27] Our user-friendly applications streamline client processes and provide clients and their employees with the ability to directly access and manage administrative processes, including applications that identify candidates, on-board employees, manage time and labor, administer payroll deductions and benefits, manage performance, terminate employees and administer post-termination health benefits such as COBRA.
[28] The widespread employee usage of our applications helps further integrate our solution into the administrative processes of our clients.
[29] Our solution also has the advantage of being built in-house by our highly trained and skilled team of software developers, thereby minimizing data integrity issues across applications.
[30] Our solution is based on a core system of record that contains payroll and HR information in one convenient database, thereby reducing costs and eliminating the need for multiple software products and vendors and the maintenance of employee data in numerous databases.
[31] This core system of record enables our clients to input employee data one time and enjoy seamless functionality across our applications.
[32] When a revision is made to the file of an employee, all appropriate personnel have access to the change in real time.
[33] In addition, our core system of record helps clients minimize the risk of compliance errors due to inaccurate or missing information that results from maintaining multiple databases.
[34] Through accurate tracking and management of employee payroll and other HR data, such information can be compiled for comprehensive and consistent reporting for our clients.
[35] Data Analytics and Business Intelligence
[36] Our solution’s core system of record allows clients to strategically analyze comprehensive and accurate employee information to make informed business decisions based upon actionable, real-time analytics provided through our client dashboard.
[37] This functionality helps our clients operate with a more complete and accurate picture of their organization, as our solution’s embedded analytics capture the content and context of everyday business events, facilitating fast and informed decision-making from any location.
[38] These tools help clients reduce administrative and operational costs and better manage talent.
[39] The employees of our clients also benefit from our HCM applications.
[40] As workforces transition from technology-savvy to technology-dependent, employees expect mobile technology and the resources necessary to readily access information and control their professional development.
```

Gate response:

```text
[]
```

#### Block 1: sentences 41–80

```text
[41] Through our employee self-service technology, employees can view real-time HR information, including pay stubs, W-2s and benefits information, as well as manage their schedules and vacation time and update W-4 contact information.
[42] Our mobile apps – available on both the App Store and Google Play – make it easier for employees to access their self-service information.
[43] Our apps have fingerprint and facial recognition capabilities, aiding employers in their efforts to engage technology-savvy workers.
[44] Our system also allows employers to engage their workforce through learning management courses and training paths, surveys and performance goals and reviews.
[45] Personalized Support Provided by Trained Personnel
[46] Our applications are supported by one-on-one personal assistance from trained specialists.
[47] Service specialists are assigned to specific clients and are trained across all of our applications, ensuring they provide comprehensive, expert-level service.
[48] Our client service is ISO 9001:2008 certified on the basis of its quality and consistency.
[49] We strive to provide our clients with high levels of service and support to ensure their continued use of our solution for all of their HCM needs.
[50] We have maintained high client satisfaction, as evidenced by an annual revenue retention rate of 91% from existing clients for each of the three years ended December 31, 2017, 2016 and 2015.
[51] Software-as-a-Service Delivery Model
[52] Our SaaS delivery model allows clients with geographically dispersed and mobile workforces to operate more efficiently, and allows these clients to implement, access and use our client-oriented internet solution on demand and remotely through standard web browsers, smart phones, tablets and other web-enabled devices.
[53] Our SaaS solution reduces the time, risk, headcount and costs associated with installing and maintaining applications for on-premise products within the information technology (“IT”) infrastructure of our clients.
[54] Secure Cloud-Based Architecture
[55] Our cloud-based architecture allows our solution to be implemented remotely with minimal client interaction.
[56] Updates such as software enhancements and newly developed applications can be deployed without client interaction, disruption or involvement, allowing our clients to make a smaller investment in hardware, personnel, implementation time and consulting.
[57] Additionally, we own and maintain all of the infrastructure technology to host our solution and to maximize system availability for clients.
[58] Our focus and investment in technology and data security has been recognized with ISO/IEC 27001:2013 certified security standards that provide our clients with a “best-in-class” level of data security.
[59] Scalability to Grow with our Clients
[60] Our solution is highly scalable.
[61] We serve a diversified client base ranging in size from one employee to many thousands of employees, although our target client size range is 50 to 2,000 employees.
[62] We calculate the number of clients’ employees based on parent company grouping.
[63] Our clients are able to use the same solution while their businesses grow by deploying applications as-needed in real-time.
[64] Pricing is determined by employee headcount and the number of applications utilized, enabling our clients to align HCM spending with their evolving HCM needs as compared to traditional HCM products that require clients to migrate to new software as they grow but retain fixed costs even if the client shrinks in size.
[65] Efficient and Productive Research and Development
[66] We believe that we benefit from a competitive advantage with our research and development investments, people and processes.
[67] Early investments in our proprietary, cloud-based architecture enable us to develop and deploy applications in a timely and cost-effective manner.
[68] We have also chosen to base our research and development team in Oklahoma and Texas, which we believe provides us with high-quality talent at a lower cost compared to other locations in the United States where there is more competition for technology talent.
[69] These strategic decisions have enabled us to have a highly productive research and development function.
[70] Our strategy is to continue to establish our solution as the HCM industry standard by increasing our presence in existing markets and expanding into additional markets.
[71] We intend to open 10 to 14 new sales offices over the next two years as well as potentially expand over the longer term into international markets.
[72] We will also execute our strategy for growth by targeting larger clients, as well as strengthening and extending our solution.
[73] Increase Our Presence in Existing Markets
[74] We believe a significant market opportunity exists to increase our presence within markets where we currently have a sales office.
[75] Each sales office is typically staffed with one sales team, with each team comprised of a sales manager and approximately six to eight other sales professionals.
[76] Although we have a sales office in 35 of the 50 largest metropolitan statistical areas (“MSAs”) in the United States based on July 2016 U.S. Census Bureau estimates, only five of these MSAs are currently served by multiple Paycom sales teams.
[77] In addition to expanding into new markets, we plan to further penetrate and more effectively capture existing markets by adding sales offices and increasing the number of sales teams in such markets.
[78] Since our initial public offering (“IPO”) in April 2014, we have expanded our presence within three MSAs that were already served by at least one Paycom sales team by opening new sales offices in Brooklyn, Chicago, Long Island and Pasadena.
[79] Expand Into Additional Markets
[80] We plan to continue expanding our sales capability by opening sales offices in certain metropolitan areas where we currently have no sales teams.
```

Gate response:

```text
[67]
```

#### Block 2: sentences 81–120

```text
[81] Since our IPO in April 2014, we have expanded into eleven new markets by opening new sales offices in Cincinnati, Cleveland, Kansas City, Milwaukee, Nashville, Pittsburgh, Richmond, Sacramento, Salt Lake City, San Antonio, and Stamford.
[82] We have historically selected new locations based on potential client and employee demographics as well as business density.
[83] When opening a new sales office, we typically relocate a proven sales manager from an existing territory who then recruits a team of high performing sales representatives.
[84] It typically takes a new sales office 24 months to reach maturity.
[85] Enlarge our Existing Client Relationships
[86] We dedicate our resources to helping our clients facilitate their goals, whether through helping them execute better hiring decisions, manage compensation more effectively or simply operate more efficiently.
[87] We believe a significant growth opportunity exists in selling additional applications to our current clients.
[88] Many clients have subsequently deployed additional applications as they recognize the benefits of our comprehensive solution.
[89] As we extend and enhance the functionality of our solution, we will continue to invest in initiatives to increase the adoption of our solution and maintain our high levels of client satisfaction.
[90] The average size of our clients has grown significantly as we have organically grown our operations and increased the number of applications we offer.
[91] Based on our total revenues, we have grown at an approximately 42% CAGR from January 1, 2013 through December 31, 2017.
[92] Our solution requires no adjustment to serve larger clients.
[93] We believe larger employers represent a substantial opportunity to increase the number of clients and to increase our revenues per client, with limited incremental cost to us.
[94] To further capitalize on this opportunity, we intend to continue targeting larger businesses opportunistically where our current sales model is effective.
[95] Maintain Our Leadership in Innovation by Strengthening and Extending our Solution
[96] Our ability to develop and deploy new applications and updates rapidly and cost-effectively has been integral to the results that we have achieved to date.
[97] We intend to continue extending the functionality and range of our solution in the future.
[98] Our development efforts are performed exclusively in-house and are heavily based upon proactive research and client input.
[99] We are focusing our investments on the development of new applications, enhancements and learning courses that are responsive to the needs of our clients, which are garnered through ongoing client interaction and collaboration.
[100] Our HCM solution offers a full suite of applications that generally fall within the following categories: talent acquisition, time and labor management, payroll, talent management and HR management.
[101] Our applicant tracking application simplifies the recruiting processes needed to hire the most qualified employees.
[102] By using our all-in-one system, our clients can move candidates from the application process through new employee on-boarding without re-keying data.
[103] Our candidate tracker application enables recruiters to track and stay connected to potential talent through an online database of top candidates.
[104] This application helps clients fill future positions faster without the cost of professional recruiting firms.
[105] Our background check application helps to ensure that prospective new hires are qualified candidates.
[106] We provide clients with the tools for authorizing background checks, creating pre-adverse and adverse action letters and securely store results as required by the Fair Credit Reporting Act.
[107] Our on-boarding application streamlines the hiring and termination processes for employees of our clients by creating online checklists of tasks to be assigned to an employee or group of employees.
[108] Our E-Verify ® application automates employment verification and reduces our clients’ exposure to audits and penalties that could result from I-9 violations.
[109] Our tax credit services application helps employers process and calculate the available federal tax credits associated with hiring employees who meet various qualifications.
[110] Our time and attendance application allows our clients to accurately and efficiently manage when, where and how employees report their hours worked.
[111] Clients can apply customized rules, use batch editing and use timecard management tools to manage complex time and attendance needs.
[112] Our Web Time Clock feature allows employees to clock in and out online, which automatically updates the payroll application when approved, eliminating the need to manually calculate timesheets and re-key information into payroll systems.
[113] We also offer several different types of hardware that are ideal for single or multi-terminal environments.
[114] Scheduling/Schedule Exchange .
[115] Our scheduling application helps managers with employee scheduling through automated functionality that provides for a seamless workflow with the payroll and time and attendance applications.
[116] Our schedule exchange application allows employees and managers access to their schedules at any time and employees can approve, decline or swap their schedules and see what shifts are available for pickup.
[117] Our time-off requests application automates and standardizes the time-off request procedure and helps employers remain effectively staffed.
[118] Managers can view an online time-off calendar to easily monitor and approve or deny time-off requests.
[119] Our employee self-service tool allows employees to view the time-off they have available, submit requests and view blackout dates, the status of requests and any manager comments.
[120] Our labor allocation application simplifies the process of setting up and tracking employee hours based on the job the employee is working.
```

Gate response:

```text
[83]
```

#### Block 3: sentences 121–160

```text
[121] Labor Management Reports/Push Reporting .
[122] Our labor management reports application provides clients with access to up-to-the-minute reports on the information they need to better manage their labor force, such as overtime and labor distribution.
[123] Our push reporting application also gives clients the ability to set up recurring reports and to schedule them to be run automatically and sent to users on a daily, weekly, monthly, quarterly or yearly basis.
[124] Enhancing our time and attendance solution, Paycom’s geofencing and geotracking location-based technology assist our clients in managing the whereabouts of employees while on the job.
[125] Geofencing allows employers to establish geographical boundaries within which their employees are authorized to clock in and out when using our Web Time Clock on smartphones, tablets or other electronic devices.
[126] Once enabled, this time-theft-combatting tool supersedes IP address restrictions, meaning the system first checks for authorized geographical locations, rather than authorized IP addresses.
[127] In addition, the geotracking tool empowers clients to track employees’ geographical locations upon clocking in and out.
[128] The coordinates collected by the application can be entered into and viewed on a Google® display map.
[129] Our payroll application is the foundation of our solution and all of our clients are required to utilize this application in order to access our other applications.
[130] Our payroll application is automatically updated with changes in employee information and offers other time saving functionality such as batch editing and effective dating.
[131] Enhanced payroll grid functionality allows clients to automate and delegate payroll functions to accelerate the processes and build additional controls.
[132] The application can be accessed at any time to make changes, run payroll and generate custom reports.
[133] We also help our clients by handling their payroll taxes and deposits, regulatory correspondence and amendments as well as assisting with penalty and interest disputes.
[134] Our Paycom Pay application eliminates the tedious job of check reconciliation by issuing checks to our clients’ employees that clear from a Paycom bank account, which helps clients eliminate potential liability and simplifies the reconciliation process.
[135] Our expense management application eliminates the manual, paper-based processes associated with employee expense reimbursement and allows employers to control and monitor expenses by setting clearly defined rules and parameters for employee reimbursement.
[136] Employees can upload receipts when submitting their expenses and access an expense dashboard where they can view the status of their submitted expenses.
[137] Our native mobile app includes mileage tracker capability, allowing employers to more accurately track and manage employees’ mileage reimbursements that are then automatically updated within our expense management application.
[138] Our garnishment management application allows clients to handle communications with garnishment payees and agencies and to calculate and track garnishment payments.
[139] Our GL Concierge application offers organizations more control and transparency into their payroll general ledger and gives finance professionals intuitive reporting, enriched audit trails, customizable file layouts and real-time alerts.
[140] Clients of all sizes can utilize a wide variety of general ledger maps along with an action-item alert system that improves the dynamics of their daily operations.
[141] Our employee self-service application improves employee engagement by empowering employees to self-manage certain transactions, obtain quick answers to frequent payroll and HR questions, access their pay history and view performance goals and reviews and total compensation reports to review their compensation and benefits package.
[142] Benefits information and paid time-off accruals also give employees the ability to make informed decisions regarding their benefit selections and time-off requests.
[143] Our compensation budgeting application provides compensation and performance information in one system, providing clients valuable workforce insight to help manage and formulate salary budgets and establish merit-based compensation increases.
[144] Our performance management application allows employees to set standardized pay grades and performance goals for positions across an organization.
[145] It also helps streamline the performance review process with online facilitation of the review process.
[146] Our executive dashboard offers powerful workforce insight for executives to access information on demand in a variety of report formats.
[147] Because we offer an all-in-one solution in a single database, the comprehensive report data provides the workforce intelligence needed to drive human capital decisions at an executive level.
[148] Paycom Learning and Course Content .
[149] Our learning management application formalizes and standardizes our clients’ training processes.
[150] Employers can create customized content utilizing videos, presentations, quizzes and surveys.
[151] It provides employees with “anytime, anywhere” access to a central knowledge base where the employee can access content, share expertise and measure his or her professional development progress.
[152] In addition to providing the ability to create and upload custom content, we created and launched our own proprietary eLearning content.
[153] Paycom Learning clients have immediate access to a library of Paycom-created learning courses, which allow employers to educate their managers and employees quickly and consistently on foundational topics such as workplace violence, discrimination and harassment prevention.
[154] Our document and task management application is designed to manage employee files and allows employees to digitally sign and view company documents.
[155] We securely store client records to meet retention requirements and protect documents from unauthorized access and other disasters that can threaten businesses.
[156] In addition, clients can assign checklists to employees for the completion of certain tasks associated with processes such as on-boarding and off-boarding.
[157] Our government and compliance application helps clients reduce exposure to violations, audits and penalties with respect to the employment laws impacting their business, such as the Family Medical Leave Act, Equal Employment Opportunity Commission and other state and federal regulations.
[158] A single database keeps our clients’ employee data consistent and enhances reporting capabilities by providing better accuracy and real-time insight.
[159] Benefits Administration/Benefits to Carrier .
[160] Our benefits administration application allows clients to customize benefit plan setup, deduction amounts, enrollment dates and new-hire waiting periods.
```

Gate response:

```text
[120]
```

#### Block 4: sentences 161–200

```text
[161] Employers are provided census and reconciliation reports to ensure they do not overpay for benefits.
[162] Employers can also update deduction amounts for all employees or groups of employees at once and automatically updates all insurance carriers for any changes.
[163] This application also provides employees with online enrollment and helps educate them and drive informed enrollment decisions for greater employee satisfaction.
[164] Our COBRA administration application protects employers from COBRA violations and the associated fines and penalties by automatically initiating compliance measures upon entry of qualifying events into the application.
[165] This application also tracks important dates, collects and remits premiums and reports on all COBRA activity.
[166] Our personnel action forms application helps our clients reduce the amount of time and paperwork required with employee changes such as pay rate, position and title changes by allowing managers to complete and approve online personnel action forms.
[167] Our surveys application allows clients to create employee surveys to help identify and resolve workplace matters that otherwise may remain undisclosed.
[168] Clients can analyze results by the demographics of the workforce and compare how results change over time.
[169] Our Affordable Care Act (“ACA”) application provides clients with access to a dashboard that tracks employee count, employee status, health care plan affordability and ACA periods all from one convenient location and enables Paycom to file IRS Forms 1094/1095-B or –C.
[170] Clients utilizing this application also have access to additional real-time compliance reports and alerts.
[171] We serve a diverse client base in terms of size and industry.
[172] We have over 20,000 clients, or approximately 11,000 clients based on parent company grouping, none of which constituted more than one-half of one percent of our revenues for the year ended December 31, 2017.
[173] We stored data for nearly 3.3 million persons employed by our clients during the year ended December 31, 2017.
[174] Many small to mid-sized companies can typically make the decision to adopt our solution more quickly than larger companies, which we believe results in a shorter sales cycle and more closely corresponds to our target sales cycle of 30 to 90 days.
[175] As a result of the nature and size of our clientele, we maintain a diversified client base and very low revenue concentration among our clients.
[176] We believe, however, that larger employers represent a substantial opportunity to increase the number of clients and to increase our revenues per client with limited incremental cost.
[177] As we attract clients at the higher end of our target client size range, we may face longer sales cycles and less predictability in completing some of our sales.
[178] The market for HCM solutions is rapidly evolving, highly competitive and subject to changing technology, shifting client needs and frequent introduction of new products and services.
[179] Our competitors range from small, regional firms to large, well-established international firms with multiple product offerings.
[180] We compete with firms that provide HCM solutions by various means.
[181] Many providers continue to deliver legacy enterprise software, but as demand for greater flexibility and access to information grows, we believe there will be increased competition in the delivery of HCM cloud-based solutions by other SaaS providers.
[182] Our competitors offer HCM solutions that may overlap with one, several or all categories of applications offered by our solution.
[183] Our talent acquisition and talent management applications compete primarily with Cornerstone OnDemand, Inc., Oracle Corporation, SAP SE and Workday, Inc.
[184] Our payroll applications, including payroll processing, compete primarily with Automatic Data Processing, Inc. (“ADP”), Ceridian HCM, Inc. (“Ceridian”), Concur Technologies, Inc., Intuit Inc., Paychex, Inc., Paylocity Holding Corporation and The Ultimate Software Group, Inc.
[185] Our HR management applications compete primarily with ADP, Ceridian, Oracle Corporation, Paychex, Inc., Paylocity Holding Corporation, SAP SE and Workday, Inc.
[186] Our time and labor management applications compete primarily with ADP, Ceridian, Kronos Incorporated, Paylocity Holding Corporation and The Ultimate Software Grou p, Inc.
[187] Our larger competitors compete with us across multiple segments.
[188] In addition, our HCM solution continues to face competition from in-house payroll and HR systems and departments as well as HR systems and software sold by third-party vendors.
[189] Competition in the HCM solutions market is primarily based on service responsiveness, product quality and reputation, breadth of service, application offering and price.
[190] The importance of these factors depends on the size of the business.
[191] Price tends to be the most important factor of competition for smaller businesses with fewer employees, while the scope of features and customization is more important to larger businesses.
[192] Regardless of a company’s size, another important factor is the implementation experience, as all organizations are seeking a streamlined and simplified process.
[193] We sell our solution exclusively through our captive sales force, substantially all of whom have a four-year college degree.
[194] We typically recruit sales candidates who have sales experience in non-HCM industries or, with respect to candidates recruited directly from colleges and universities, who have demonstrated an aptitude for sales.
[195] Our sales force is comprised of inside sales and field sales personnel, who are organized geographically, and client relations representatives (“CRRs”), who sell additional applications to existing clients.
[196] As of the filing of this Form 10-K, we have 46 sales teams located in 26 states and plan to open additional sales offices to further expand our presence in the U.S. market.
[197] We provide our sales force with an intensive six-week training course that includes at least one week of training at our headquarters in Oklahoma City.
[198] Our unique training program includes instruction in accounting, business metrics, application features and tax matters relevant to our target market and we believe it fosters loyalty and helps maintain our corporate culture.
[199] Our training continues for our sales force through weekly in-office strategy sessions and leadership development training.
[200] Executive sales representatives are also required to attend in-person quarterly conferences to share best practices and receive legal and business updates.
```

Gate response:

```text
[]
```

#### Block 5: sentences 201–240

```text
[201] When a new client processes payroll with us for an entire month, or an existing client purchases and then utilizes a new application for one month, our sales representative or CRR receives a one-time commission based upon an estimate of future annual revenues from such client.
[202] Executive sales representatives receive a higher commission rate and base salary based upon both current year and life-to-date realized sales, respectively.
[203] We generate client leads, accelerate sales opportunities and build brand awareness through our marketing programs that target senior finance and HR executives, technology professionals and senior business leaders of companies that perform HCM functions in-house or outsource these functions to one of our competitors.
[204] Our marketing programs include:
[205] Podcasts, webinars, white papers and infographics;
[206] National and local television commercial campaigns, personalized direct mail campaigns, email campaigns, social and digital media campaigns, industry-specific advertising and tradeshow exhibiting; and
[207] Search engine marketing methods that include site optimization and pay-per-click searches.
[208] In addition to managing client relationships, our CRRs are focused on expanding the number of applications our clients purchase from us by introducing them to additional applications.
[209] Our CRRs call upon select clients periodically and are paid a non-recurring commission on any additional sales they generate.
[210] Technology, Operations and Security
[211] Our multi-tenant architecture enables us to deliver our solution across our client base with a single instance of our solution, while securely partitioning access to our clients’ respective application data.
[212] Because a single version of our solution is developed, supported and deployed across all of our clients, updates are delivered to all of our clients at the same time, making it easier to scale our solution as our number of clients and their respective employee headcounts increase.
[213] We maintain multiple load-balanced internet lines serviced by multiple networks to provide our clients continuous access to our solution and their stored data.
[214] We back up our client data at regular intervals utilizing live replication, snapshots and cold archive methods of backup and manually monitor backup success and failure regularly.
[215] Our server cluster and database servers have redundant “hot swappable” disks to ensure continuous service in the event of a disk failure.
[216] We physically host our solution for our clients in two secure data center facilities located in Oklahoma and Texas.
[217] All of our critical systems are fully redundant and backed-up in real-time to these facilities.
[218] Physical security includes ID-oriented access control, alarm systems and manned 24-hour-a-day camera monitoring by our security guards.
[219] Server facilities also have environmental monitoring and extensive environmental controls such as heat and fire protection, moisture, temperature, and humidity sensors, backup power supply and exterior reinforced concrete walls.
[220] We maintain a formal and comprehensive security program designed to ensure the confidentiality, integrity and availability of our clients’ data.
[221] During the regular course of business, we receive client data through our online system that we in turn process, record and store following ISO/IEC 270001:2013 certified controls and procedures.
[222] All communications with our servers that might contain sensitive information are encrypted before they leave the network and our servers are configured to only allow high-grade encryption algorithms.
[223] We strictly regulate and limit all access to servers and networks at each of our facilities.
[224] Local network access is restricted by our authenticated server, using access control lists and remote network access is restricted by a firewall, which provides no accessible route from external networks to systems within our local network.
[225] We also employ network and host intrusion detection and prevention sensors throughout our infrastructure, systems that monitor that infrastructure and alert our security department of cybersecurity issues, a system for managing and installing patches for unsecure third-party applications and highly restricted access to the internet for anyone who has access to client data.
[226] Our information security department regularly performs penetration testing and we retain a third-party penetration testing company to conduct penetration tests and periodic audits to identify and remediate any issues.
[227] Our applications are secured using multiple libraries and secure coding practices.
[228] Our IT infrastructure is secured and monitored using a number of best practices and tools at multiple layers of the physical and logical network.
[229] This security is also continually monitored by our information security department.
[230] All of our operations employees work in either our Oklahoma or Texas locations and, with the exception of certain IT personnel, are not permitted to work remotely.
[231] Our application development team works closely with our clients to enhance our existing application offerings and develop new applications.
[232] This process is led by experienced product managers who oversee the evolution of their respective applications within a focused timeframe of innovation and cultivation in order to deliver the well-developed applications and enhancements desired by our clients.
[233] Our product managers, many of whom are former HR executives, are proactive in their approach to assigning development requests based on research, trends and user feedback.
[234] A key element of our development process is the one-on-one personal interaction between clients and our CRRs, through whom our clients personally suggest new applications and features.
[235] We develop our solution from the “ground up” with our internal development and engineering teams.
[236] Our development and engineering teams and our employees conceive new applications and enhancements, review requests, schedule development in order of priority and subsequently develop the applications or enhancements.
[237] Our new applications and enhancements are independently reviewed by the quality assurance team, in accordance with our software development process, before being fully implemented.
[238] Any enhancements to our applications are released on a monthly scheduled release date to coordinate the communication and release to our clients.
[239] Capitalized software development expenses, which include compensation for employees directly associated with development projects, were $15.8 million, $8.8 million and $4.3 million for the years ended December 31, 2017, 2016 and 2015, respectively.
[240] We are committed to providing industry-leading, client-centered service.
```

Gate response:

```text
[61, 65, 68, 93]
```

Confirm response:

```text
[]
```

#### Block 6: sentences 241–280

```text
[241] For this reason, we assign each client a specialist within a dedicated team.
[242] This one-on-one service is a key part of our client service model and helps to ensure that we are delivering an industry-leading solution and maintaining high client satisfaction.
[243] The primary elements of our client service model include the following:
[244] Streamlined Setup and On-Boarding
[245] After electing to deploy our solution, a new client begins our on-boarding process with assistance from a team of new client setup specialists and the sales professional responsible for obtaining the client’s business.
[246] In addition, we also have a team of transition specialists whose job it is to ensure that the process is performed smoothly, data is collected properly and all relevant employees are fully trained on the system.
[247] This team works closely with the client until the client is capable of managing our solution independently, at which time responsibility for the client relationship is transferred to our dedicated CRRs and service specialists.
[248] Unlike certain of our competitors, we do not outsource any of our on-boarding efforts.
[249] After completing the on-boarding process, each client is assigned to a services specialist within a dedicated team.
[250] Clients can then contact their dedicated services specialist or a team member if any issues or questions arise.
[251] These specialists provide personalized service with actual knowledge of the clients’ business needs.
[252] When appropriate, client questions can be elevated to the specialists with the appropriate application, regulatory or tax expertise.
[253] In addition, our CRRs proactively contact our clients to ensure satisfaction with our solution and introduce additional applications.
[254] Our client specialists are trained across all of our applications to ensure that they can provide comprehensive, expert-level service.
[255] Our client service is ISO 9001:2008 certified and helps support a high client retention rate.
[256] We are subject to varying degrees of regulations in each of the jurisdictions in which we provide services.
[257] Local laws and regulations, and their interpretation and enforcement, differ significantly among those jurisdictions.
[258] These regulations and laws cover, among others, information privacy.
[259] Data privacy has become a significant issue in the United States and in other countries.
[260] The regulatory framework for privacy issues worldwide is rapidly evolving and is likely to remain uncertain for the foreseeable future.
[261] Many federal, state and foreign government bodies and agencies have adopted or are considering adopting laws and regulations affecting or regarding the collection, use and disclosure of personal information.
[262] In the United States, these include, for example, rules and regulations promulgated under the authority of the Federal Trade Commission, the Health Insurance Portability and Accountability Act of 1996, the Family Medical Leave Act of 1993, the ACA and state breach notification laws.
[263] We voluntarily obtain third-party security examinations relating to security and data privacy in accordance with Statement on Standards for Attestation Engagements (“SSAE”), No. 16, Reporting on Controls at a Service Organization.
[264] Our SSAE examination is conducted every six months by one of the four largest independent international auditing firms, and addresses, among other areas, our physical and environmental safeguards for production data centers, data availability and integrity procedures, change management procedures and logical security procedures.
[265] In October 2016, we renewed a certification based on ISO/IEC 27001:2013 criteria, a security standard for Information Security Management Systems published by ISO covering our production, quality assurance and implementation environments.
[266] This independent assessment of our conformity to the ISO 27001 standard includes assessing security risks, designing and implementing comprehensive security controls and adopting an information security management process to meet security needs on an ongoing basis.
[267] The certification is valid until December 2019, with continuing assessments taking place annually.
[268] In April 2017, we renewed a certification based on ISO 9001:2008 criteria, a standard for the implementation of quality management processes published by ISO, covering our activities required to create and deliver our solution.
[269] This independent assessment of our conformity to the ISO 9001:2008 standard includes assessing the design and implementation of quality objectives to meet delivery standards on an ongoing basis.
[270] The certification is valid until September 2018, with continuing assessments taking place annually.
[271] We rely on a combination of copyrights, trademarks, service marks, trade secret laws and contractual restrictions to establish and protect our intellectual property rights.
[272] We also have a number of registered and unregistered trademarks and will continue to evaluate the registration of additional trademarks as appropriate.
[273] We do not have any patents or patent applications pending.
[274] Our revenues are seasonal in nature.
[275] Recurring revenues include revenues relating to the annual processing of payroll forms, such as Form W-2 and Form 1099, and revenues from processing unscheduled payroll runs (such as bonuses) for our clients.
[276] Because payroll forms are typically processed in the first quarter of the year, first quarter revenues and margins are generally higher than in subsequent quarters.
[277] Further, beginning in the first quarter of 2016, we began generating additional revenues as a result of the enactment of the ACA, as many clients began complying with filing requirements for Forms 1094 and 1095.
[278] We anticipate that our revenues will continue to exhibit this seasonal pattern related to ACA form filings for so long as the ACA (or replacement legislation) includes employer reporting requirements.
[279] In addition, we often experience increased revenues during the fourth quarter due to unscheduled payroll runs for our clients that occur before the end of the year.
[280] Therefore, we expect the seasonality of our revenue cycle to decrease to the extent clients utilize more of our non-payroll applications.
```

Gate response:

```text
[65, 68, 69]
```

Confirm response:

```text
[[258, 68, "T"], [259, 68, "T"], [260, 68, "T"], [261, 68, "T"], [262, 68, "T"], [263, 68, "O"], [264, 68, "O"], [265, 68, "O"], [266, 68, "O"], [267, 68, "O"], [268, 68, "O"], [269, 68, "O"], [270, 68, "O"]]
```

#### Block 7: sentences 281–300

```text
[281] Our ability to recruit and retain qualified employees is critical to our continued success.
[282] We invest heavily in our training and leadership development programs to encourage the development and promotion of our employees.
[283] As of December 31, 2017, we employed 2,548 people.
[284] None of our employees were covered by collective bargaining agreements.
[285] Our corporate headquarters is an approximately 250,000-square-foot campus located on over 30 acres of Company-owned property in Oklahoma City, Oklahoma.
[286] In addition to housing a fully redundant data center at our corporate headquarters, we operate another fully redundant data center at a leased property near Dallas, Texas.
[287] We also lease a disaster recovery site in downtown Oklahoma City.
[288] We also lease offices in Arizona, California, Colorado, Connecticut, Florida, Georgia, Illinois, Indiana, Maryland, Massachusetts, Michigan, Minnesota, Missouri, New Jersey, New York, North Carolina, Ohio, Oklahoma, Oregon, Pennsylvania, Tennessee, Texas, Utah, Virginia, Washington and Wisconsin.
[289] We believe that these facilities are suitable for our current operations and upon the expiration of the terms of the leases we believe we could renew these leases or find suitable space elsewhere on acceptable terms.
[290] We operate in a single operating segment and a single reporting segment.
[291] Operating segments are defined as components of an enterprise about which separate financial information is regularly evaluated by the chief operating decision maker function (which is fulfilled by our chief executive officer) in deciding how to allocate resources and in assessing performance.
[292] Our chief executive officer allocates resources and assesses performance based upon financial information at the consolidated level.
[293] Since we operate in one operating segment, all required financial segment information is presented in the consolidated financial statements.
[294] Our internet address is www.paycom.com and our investor relations website is located at investors.paycom.com.
[295] Our Annual Reports on Form 10-K, Quarterly Reports on Form 10-Q, Current Reports on Form 8-K and amendments to those reports can be found on our Investor Relations website, free of charge.
[296] These reports are also electronically filed with (or furnished to) the SEC.
[297] Information contained on our website is not incorporated by reference into this Form 10-K.
[298] The SEC maintains a public website, www.sec.gov, which includes information about and the filings of issuers that file electronically with the SEC.
[299] Additionally, the information that we file with the SEC may be read at the SEC’s Public Reference Room at 100 F Street NE, Washington, DC 20549.
[300] Information about the SEC’s Public Reference Room may be obtained by calling the SEC at 1-800-SEC-0330.
```

Gate response:

```text
[]
```

<a id="0001136893-18-000011"></a>
## Fidelity National (FIS)

Opportunity rank 2/894; 3/259 opportunity sentences (1.16%); all recorded counts: threat 24, neutral 1, opportunity 3.

NAICS 518. Filed 2018-02-22; 46 days before hearing. [SEC filing](https://www.sec.gov/Archives/edgar/data/1136893/000113689318000011/a10-k2017.htm); [saved Item 1](<../../01 - Inputs/Source Filings/0001136893-18-000011_source.txt>).

Aliases searched and match counts: {'Fidelity National Information Services': 0, 'FIS': 0}.

Context, sentence 215: The proposed EU data protection regime imposes a strict data compliance regime and extends the scope of the EU data protection law to all foreign companies processing data of EU residents.

**Selected sentence 217 / recorded label opportunity:** The Company has adopted a comprehensive global privacy program to assess and manage these evolving risks, including contract terms to comply with this new law.

Interpretation: The program manages privacy risks and compliance. A business gain is not explicitly stated, so the opportunity label requires review.

All model tags are retained below, including statements that may concern neighboring subjects or support a different directional interpretation. No counts or ranks are manually corrected.

### All retained tags

| Sentence | Recorded label | Original text |
|---:|---|---|
| 169 | threat | Our services are subject to a broad range of complex federal, state, and foreign regulation and requirements, as well as requirements under the rules of self-regulatory organizations, including federal truth-in-lending and truth-in-savings rules, Regulation AA (Unfair or Deceptive Acts or Practices), data protection and privacy laws, usury laws, laws governing state trust charters, the Equal Credit Opportunity Act, the Electronic Funds Transfer Act, the Fair Credit Reporting Act, the Fair Debt Collection Practices Act, the Bank Secrecy Act, the USA Patriot Act, the Internal Revenue Code, the Employee Retirement Income Security Act, the Health Insurance Portability and Accountability Act, the Community Reinvestment Act and the Dodd-Frank Wall Street Reform and Consumer Protection Act (the "Dodd-Frank Act"), the Securities Exchange Act of 1934 (the "1934 Act"), the Investment Advisors Act of 1940 (the "1940 Act"), the U.S. Foreign Corrupt Practices Act and UK Bribery Act, and the rules and regulations of the Financial Industry Regulatory Authority (“FINRA”), the Securities and Exchange Commission (“SEC”) and the Financial Conduct Authority in the U.K. (“FCA”). |
| 202 | threat | The Company is subject to a number of privacy and data protection laws, regulations and directives globally (referred to collectively as “Privacy Laws”), many of which place restrictions on the Company’s ability to efficiently transfer, access and use personal data across its business. |
| 203 | threat | The legislative and regulatory landscape for privacy and data protection continues to evolve. |
| 204 | threat | Our financial institution clients operating in the United States are required to comply with privacy regulations imposed under the Gramm-Leach-Bliley Act (referred to as “GLBA”). |
| 205 | threat | GLBA places restrictions on the use of non-public personal information. |
| 206 | threat | All financial institutions must disclose detailed privacy policies to their customers and offer them the opportunity to direct the financial institution not to share information with third parties. |
| 207 | threat | The regulations under GLBA, however, permit financial institutions to share information with non-affiliated parties who perform services for the financial institutions. |
| 208 | threat | As a provider of services to financial institutions, we are required to comply with the privacy laws and are bound by the same limitations on disclosure of the information received from our clients as apply to the financial institutions themselves. |
| 209 | threat | A determination that there have been violations of privacy laws could expose us to significant damage awards, fines and other penalties that could, individually or in the aggregate, materially harm our business and reputation. |
| 210 | threat | In October 2015, the European Court of Justice ruled that the U.S.-EU Safe Harbor framework clauses, a compliance method by which we relied in portions of our business to transfer personal data regarding citizens of the EU to the U.S., could no longer be relied upon. |
| 211 | threat | The U.S. and EU authorities have agreed in principle on a replacement for Safe Harbor known as “Privacy Shield”. |
| 212 | threat | The Privacy Shield approach has not been fully endorsed by all relevant parties and there have already been challenges to this initiative in the European justice system. |
| 213 | threat | While we have certified certain lines of business under the Privacy Shield, we have chosen to adopt EU model clauses published by the European Commission as the primary basis for the export of data from the EU to the U.S. |
| 214 | threat | The EU has recently adopted a comprehensive overhaul of its data protection regime from the current national legislative approach to a single European Economic Area Privacy Regulation, the General Data Protection Regulation (“GDPR”), which comes into effect on May 26, 2018. |
| 215 | threat | The proposed EU data protection regime imposes a strict data compliance regime and extends the scope of the EU data protection law to all foreign companies processing data of EU residents. |
| 216 | threat | Although the GDPR will apply across the EU without a need for local implementing legislation, as has been the case under the current data protection regime, local data protection authorities (“DPAs”) will still have the ability to interpret the GDPR, which has the potential to create inconsistencies on a country-by-country basis. |
| 217 | opportunity | The Company has adopted a comprehensive global privacy program to assess and manage these evolving risks, including contract terms to comply with this new law. |
| 228 | neutral | Consumer Reporting and Protection. |
| 229 | threat | Our retail check authorization services (Certegy Check Services) and account opening services, including credit scoring analysis (ChexSystems), maintain databases of consumer information and, as a consequence, are subject to the Federal Fair Credit Reporting Act and similar state laws. |
| 230 | threat | Among other things, the Federal Fair Credit Reporting Act imposes requirements on us concerning data accuracy, and provides that consumers have the right to know the contents of their files, to dispute their accuracy, and to require verification or removal of disputed information. |
| 231 | threat | The Federal Trade Commission (FTC), as well as state attorneys general and other agencies, have enforcement responsibility over the collection laws, as well as the various credit reporting laws. |
| 232 | opportunity | In furtherance of our objectives of data accuracy, fair treatment of consumers, protection of consumers’ personal information, and compliance with these laws, we strive to, and have made considerable investment to, maintain a high level of security for our computer systems in which consumer data resides, and we maintain consumer relations call centers to facilitate efficient handling of consumer requests for information and handling disputes. |
| 233 | opportunity | We also are focused on ensuring our operating environments safeguard and protect consumer's personal information in compliance with these laws. |
| 234 | threat | Our consumer reporting and facing businesses are subject to CFPB bulletin 2013-7 (an update to the former Regulation A- Unfair Deceptive Acts or Practices), which states the definition of Unfair, Deceptive or Abusive Acts or Practices (UDAAP). |
| 235 | threat | This specific bulletin states that UDAAPs can cause significant financial injury to consumers, erode consumer confidence, and undermine fair competition in the financial marketplace. |
| 236 | threat | Original creditors and other covered persons and service providers under the Dodd-Frank Act involved in collecting debt related to any consumer financial product or service are subject to the prohibition against UDAAPs in the Dodd-Frank Act. |
| 237 | threat | Our collection services supporting our check, card and payment environments are subject to the Federal Fair Debt Collection Practices Act and various state collection laws and licensing requirements. |
| 238 | threat | Trade Commission, as well as state attorneys general and other agencies, have enforcement responsibility over the collection laws, as well as the various credit reporting laws. |

### Complete input blocks and recorded responses

#### Block 0: sentences 1–40

```text
[1] FIS is a global leader in financial services technology with a focus on retail and institutional banking, payments, asset management and wealth and retirement, risk and compliance and outsourcing solutions.
[2] Through the depth and breadth of our solutions portfolio, global capabilities and domain expertise, FIS serves more than 20,000 clients in over 130 countries.
[3] Headquartered in Jacksonville, Florida, FIS employs more than 53,000 people worldwide and holds leadership positions in payment processing, financial software and banking solutions.
[4] Providing software, services and outsourcing of the technology that empowers the financial world, FIS is a Fortune 500 company and is a member of the Standard & Poor’s 500 ® Index.
[5] FIS is incorporated under the laws of the State of Georgia as Fidelity National Information Services, Inc. and our stock is traded on the New York Stock Exchange under the trading symbol "FIS".
[6] We have grown organically, as well as through acquisitions, which have contributed critical applications and services that complement or enhance our existing offerings, diversifying our revenues by customer, geography and service offering.
[7] These acquired offerings include integrated core banking and payment solutions, mobile banking solutions, item processing services, card issuer services, risk management solutions, electronic loan amendment applications and services, electronic funds transfer ("EFT") services, merchant acquiring services, and prepaid/gift card processing for community banks, credit unions, and other financial institutions.
[8] We sell many of these solutions to domestic companies, as well as to global organizations and companies domiciled both within and outside of North America, where our solutions are able to be deployed across multiple regions.
[9] Our strategic acquisitions have enabled us to broaden our available solution sets, scale our operations, expand and diversify our customer base and strengthen our competitive position.
[10] On November 30, 2015, FIS acquired SunGard (the "SunGard acquisition").
[11] The SunGard acquisition increased our existing portfolio of solutions to automate a wide range of complex business processes to financial services institutions and corporate and government treasury departments, adding solutions for trading, securities operations, administering investment portfolios, accounting for investment assets, and managing risk and compliance requirements.
[12] The combination of FIS and SunGard brought together complementary technology solutions and services to enable a broader technology platform serving our existing and future clients.
[13] Financial Information About Operating Segments and Geographic Areas
[14] In 2015, FIS finalized a reorganization and began reporting its financial performance based on three segments: Integrated Financial Solutions (“IFS”), Global Financial Solutions (“GFS”) and Corporate and Other.
[15] We recast all previous periods to conform to the new segment presentation.
[16] Following our November 30, 2015 acquisition of SunGard, the SunGard business was included within the GFS segment as its economic characteristics, international business model, and various other factors largely aligned with those of our GFS segment.
[17] As we further integrated the acquired SunGard businesses through March 31, 2016, we reclassified certain SunGard businesses (corporate liquidity and wealth and retirement) that are oriented more to the retail banking and payments activities of IFS into that segment.
[18] Certain other businesses from both SunGard (the public sector and education businesses, which were divested in February 2017), and legacy FIS (global commercial services and retail check processing) were reclassified to the Corporate and Other segment, as were SunGard administrative expenses.
[19] Prior periods were reclassified to conform to the current segment presentation.
[20] For information about our revenues and assets by geographic area see Notes 2(n) and 19 of the Notes to Consolidated Financial Statements.
[21] We believe our competitive strengths include the following:
[22] Brand - FIS has built a global brand known for innovation and thought leadership in the financial services sector.
[23] Global Distribution and Scale - Our worldwide presence, array of solution offerings, customer breadth, established infrastructure and employee depth enable us to leverage our client relationships and global scale to drive revenue growth and operating efficiency.
[24] We are a global leader in the markets we serve, supported by a large, knowledgeable talent pool of employees around the world.
[25] Extensive Domain Expertise and Extended Portfolio Depth - FIS has a significant number and wide range of high-quality software applications and service offerings that have been developed over many years with substantial input from our customers.
[26] Our broad portfolio of solutions includes a wide range of flexible service arrangements for the deployment and support of our software, from managed processing arrangements, either at the customer's site or at an FIS location, to traditional license and maintenance fee approaches.
[27] This broad solution set allows us to bundle tailored or integrated services to compete effectively.
[28] In addition, FIS is able to use the modular nature of our software applications and our ability to integrate many of our services with the services of others to provide customized solutions that respond to individualized customer needs.
[29] We understand the needs of our customers and have developed and acquired innovative solutions that can give them a competitive advantage and reduce their operating costs.
[30] Excellent Relationship with Customers - A significant percentage of FIS’ business with our customers relates to applications and services provided under multi-year, recurring contracts.
[31] The nature of these relationships allows us to develop close partnerships with these customers, resulting in high client retention rates.
[32] As the breadth of FIS’ service offerings has expanded, we have found that our access to key customer personnel is increasing, presenting greater opportunities for cross-selling and providing integrated, total solutions to our customers.
[33] Our mission is to deliver superior solutions and services to our clients, which will result in sustained revenue and earnings growth for our shareholders.
[34] Our strategy to achieve this goal has been and continues to be built on the following pillars:
[35] Build, Buy, or Partner to Add Solutions to Cross-Sell - We continue to invest in growth through internal software development, as well as through acquisitions and equity investments that complement and extend our existing solutions and capabilities, providing us with additional solutions to cross-sell.
[36] We also partner from time to time with other entities to provide comprehensive offerings to our prospects and customers.
[37] By investing in solution innovation and integration, we continue to expand our value proposition to our prospects and clients.
[38] Support Our Clients Through Innovation - Changing market dynamics, particularly in the areas of information security, regulation and innovation, are transforming the way our clients operate, which is driving incremental demand for our integrated solutions and services around our intellectual property.
[39] As prospects and customers evaluate technology, business process changes and vendor risks, our depth of services capabilities enables us to become involved earlier in their planning and design process and assist them as they manage through these changes.
[40] Continually Improve to Drive Margin Expansion - We strive to optimize our performance through investments in infrastructure enhancements, our workforce and other measures that are designed to drive margin expansion.
```

Gate response:

```text
[]
```

#### Block 1: sentences 41–80

```text
[41] Expand Client Relationships - The overall market we serve continues to gravitate beyond single-application purchases to multi-solution partnerships.
[42] As the market dynamics shift, we expect our clients and prospects to rely more on our multidimensional service offerings.
[43] Our leveraged solutions and processing expertise can produce meaningful value and cost savings for our clients through more efficient operating processes, improved service quality and convenience for our clients' customers.
[44] Build Global Diversification - We continue to deploy resources in global markets where we expect to achieve meaningful scale.
[45] The table below summarizes our revenues by reporting segment (in millions):
[46] Integrated Financial Solutions ("IFS")
[47] The IFS segment is focused primarily on serving North American regional and community bank and savings institutions for transaction and account processing, payment solutions, channel solutions, digital channels, fraud, risk management and compliance solutions, lending and wealth and retirement solutions, and corporate liquidity, capitalizing on the continuing trend to outsource these solutions.
[48] Clients in this segment include regional and community banks, credit unions and commercial lenders, as well as government institutions, merchants and other commercial organizations.
[49] These markets are primarily served through integrated solutions and characterized by multi-year processing contracts that generate highly recurring revenues.
[50] The predictable nature of cash flows generated from this segment provides opportunities for further investments in innovation, integration, information and security, and compliance in a cost-effective manner.
[51] Our solutions in this segment include:
[52] Core Processing and Ancillary Applications.
[53] Our core processing software applications are designed to run banking processes for our financial institution clients, including deposit and lending systems, customer management, and other central management systems, serving as the system of record for processed activity.
[54] Our diverse selection of market-focused core systems enables FIS to compete effectively in a wide range of markets.
[55] We also offer a number of services that are ancillary to the primary applications listed above, including branch automation, back-office support systems and compliance support.
[56] Digital Solutions, Including Internet, Mobile and eBanking.
[57] Our comprehensive suite of retail delivery applications enables financial institutions to integrate and streamline customer-facing operations and back-office processes, thereby improving customer interaction across all channels (e.g., branch offices, Internet, ATM, Mobile, call centers).
[58] FIS' focus on consumer access has driven significant market innovation in this area, with multi-channel and multi-host solutions and a strategy that provides tight integration of services and a seamless customer experience.
[59] FIS is a leader in mobile banking solutions and electronic banking enabling clients to manage banking and payments through the Internet, mobile devices, accounting software and telephone.
[60] Our corporate electronic banking solutions provide commercial treasury capabilities including cash management services and multi-bank collection and disbursement services that address the specialized needs of corporate clients.
[61] FIS systems provide full accounting and reconciliation for such transactions, serving also as the system of record.
[62] Fraud, Risk Management and Compliance Solutions.
[63] Our decision solutions offer a spectrum of options that cover the account lifecycle from helping to identify qualified account applicants to managing existing customer accounts and fraud.
[64] Our applications include know-your-customer, new account decisioning and opening, account and transaction management, fraud management and collections.
[65] Our risk management services use our proprietary risk management models and data sources to assist in detecting fraud and assessing the risk of opening a new account.
[66] Our systems use a combination of advanced authentication procedures, predictive analytics, artificial intelligence modeling and proprietary and shared databases to assess and detect fraud risk for deposit transactions for financial institutions.
[67] We also provide outsourced risk management and compliance solutions that are configurable to a client's regulatory and risk management requirements.
[68] Electronic Funds Transfer and Network Services.
[69] Our electronic funds transfer and debit card processing businesses offer settlement and card management solutions for financial institution card issuers.
[70] We provide traditional ATM-based debit network access through NYCE and emerging real-time payment alternatives.
[71] NYCE connects millions of cards and point-of-sale locations nationwide, providing consumers with secure, real-time access to their money.
[72] Also through NYCE, clients such as financial institutions, retailers and independent ATM operators can capitalize on the efficiency, consumer convenience and security of electronic real-time payments, real-time account-to-account transfers, and strategic alliances such as surcharge-free ATM network arrangements.
[73] Approximately 5,600 financial institutions use a combination of our technology and/or services to issue VISA ® , MasterCard ® or American Express ® branded credit and debit cards or other electronic payment cards for use by both consumer and business accounts.
[74] Card transactions continue to increase as a percentage of total point-of-sale payments, which fuels continuing demand for card-related services.
[75] We offer Europay, MasterCard and VISA ("EMV") integrated circuit cards, often referred to as smart cards or chip cards, as well as a variety of stored-value card types and loyalty/reward programs.
[76] Our integrated services range from card production and activation to processing to an extensive range of fraud management services and value-added loyalty programs designed to increase card usage and fee-based revenues for financial institutions and merchants.
[77] The majority of our programs are full service, including most of the operations and support necessary for an issuer to operate a credit card program.
[78] We do not make credit decisions for our card issuing clients.
[79] We are also a leading provider of prepaid card services, which include gift cards and reloadable cards, with end-to-end solutions for development, processing and administration of stored-value programs.
[80] Our closed loop gift card solutions and loyalty programs provide merchants compelling solutions to drive consumer loyalty.
```

Gate response:

```text
[48, 54, 61, 67, 68, 94]
```

Confirm response:

```text
[]
```

#### Block 2: sentences 81–120

```text
[81] In addition, our merchant processing service provides a merchant or financial institution a comprehensive solution to manage its merchant card activities, including point-of-sale equipment, transaction authorization, draft capture, settlement, charge-back processing and reporting.
[82] Our corporate liquidity solutions help chief financial officers and treasurers manage working capital by increasing visibility to cash, reducing risk and improving communication and response time between a company’s buyers, suppliers, banks and other stakeholders.
[83] Our end-to-end collaborative financial management framework helps bring together receivables, treasury and payments for a single view of cash and risk, which helps our clients optimize business processes for enhanced liquidity management.
[84] We provide wealth and retirement solutions that help banks, trust companies, brokerage firms, insurance firms, retirement plan professionals, benefit administrators and independent advisors acquire, service and grow their client relationships.
[85] We provide solutions for client acquisition, transaction management, trust accounting and recordkeeping that can be deployed stand-alone or as part of an integrated wealth or retirement platform, or on an outsourced basis.
[86] Item Processing and Output Services.
[87] Our item processing services furnish financial institutions with the technology needed to capture data from checks, transaction tickets and other items; image and sort items; process exceptions through keying; and perform balancing, archiving and the production of statements.
[88] Our item processing services are performed at one of our multiple item processing centers located throughout the U.S. or on-site at client locations.
[89] Our extensive solutions include distributed (i.e., non-centralized) data capture, mobile deposit capture, check and remittance processing, fraud detection, and document and report management.
[90] Clients encompass banks and corporations of all sizes, from de novo banks to the largest financial institutions and corporations.
[91] We offer a number of output services that are ancillary to the primary solutions we provide, including print and mail capabilities, document composition software and solutions, and card personalization fulfillment services.
[92] Our print and mail services offer complete computer output solutions for the creation, management and delivery of print and fulfillment needs.
[93] We provide our card personalization fulfillment services for branded credit cards and branded and non-branded debit and prepaid cards.
[94] Government Payments Solutions.
[95] We provide comprehensive, customized electronic service applications for government agencies, including Internal Revenue Service (IRS) payment services and government food stamp and nutrition programs known as Supplemental Nutrition Assistance Program (“SNAP”) and Women, Infants and Children ("WIC").
[96] We also facilitate the collection of state income taxes, real estate taxes, utility bills, vehicle registration fees, driver’s license renewal fees, parking tickets, traffic citations, tuition payments, court fees and fines, hunting and fishing license fees, as well as various business licenses.
[97] We provide reliable and scalable bill publishing and bill consolidation technology for our clients, generating and facilitating the payment of millions of monthly bills, servicing both billers and financial institution clients.
[98] Online bill payment functionality includes credit and debit card-based expedited payments.
[99] Our end-to-end presentment and payment solution provides an all-in-one solution to meet billers’ needs for the distribution and collection of bills and other customer documents.
[100] FIS also provides Automated Clearing House ("ACH") processing.
[101] Global Financial Solutions ("GFS")
[102] The GFS segment is focused on serving the largest global financial institutions and/or international financial institutions with a broad array of capital markets (including asset managers, buy- and sell-side securities and trading firms), asset management and insurance solutions, as well as banking and payments solutions.
[103] GFS clients include the largest global financial institutions, including those headquartered in the United States, as well as international financial institutions we serve as clients in more than 130 countries around the world, and asset managers, buy-and sell-side securities and trading firms, insurers and private equity firms.
[104] These institutions face unique business and regulatory challenges and account for the majority of financial institution information technology spend globally.
[105] The purchasing patterns of GFS clients vary from those of IFS clients who typically purchase solutions on an outsourced basis.
[106] GFS clients purchase our solutions and services in various ways including licensing and managing technology “in-house”, using consulting and third-party service providers as well as fully outsourced end-to-end solutions.
[107] We have long-established relationships with many of these financial institutions that generate significant recurring revenue.
[108] This segment also includes the Company's consolidated Brazilian Venture (see Note 17 of the Notes to Consolidated Financial Statements).
[109] Our solutions in this segment include:
[110] Securities Processing and Finance.
[111] Our offerings help financial institutions to increase the efficiency, transparency and control of their back-office trading operations, post-trade processing and settlement including derivative solutions, risk management, securities lending, syndicated lending, tax processing, and regulatory compliance.
[112] The breadth of our offerings also facilitates advanced business intelligence and market data distribution based on our extensive market data access.
[113] Our trading solutions provide trade execution, data and network solutions to financial institutions, corporations and municipalities in North America, Europe and other global markets across a variety of asset classes.
[114] Our trade execution and network solutions help both buy- and sell-side firms improve execution quality, decrease overall execution costs and address today’s trade connectivity challenges.
[115] Asset Management and Insurance .
[116] We offer solutions that help institutional investors, insurance companies, hedge funds, private equity firms, fund administrators and securities transfer agents improve both investment decision-making and operational efficiency, while managing risk and increasing transparency.
[117] Our asset management solutions support every stage of the investment process, from research and portfolio management, to valuation, risk management, compliance, investment accounting, transfer agency and client reporting.
[118] Our insurance solutions help support front-office and back-office functions including actuarial risk calculations, policy administration and financial and investment accounting and reporting for a variety of insurance lines, including life and health, annuities and pensions, property and casualty, reinsurance, and asset management.
[119] Retail Banking and Payments Services.
[120] Our GFS operations leverage existing applications and provide services for the specific business needs of our customers in targeted global markets.
```

Gate response:

```text
[]
```

#### Block 3: sentences 121–160

```text
[121] Services are delivered from our operation centers around the world.
[122] Our banking solution services include fully outsourced core bank processing arrangements, application management, software licensing and maintenance and facilities management.
[123] Our payment solution services include fully outsourced card-issuer services and customer support, payment processing (including real-time payments) and switching services, prepaid and debit card processing, software licensing and maintenance, outsourced ATM management and retail point-of-sale payment services.
[124] Strategic Consulting Services.
[125] We completed the sale of a majority stake in Capco, which comprised our Strategic Consulting Services, on July 31, 2017.
[126] (see Note 15 of the Notes to Consolidated Financial Statements).
[127] The Corporate and Other segment consists of corporate overhead expense, certain leveraged functions and miscellaneous expenses that are not included in the operating segments, as well as certain non-strategic businesses.
[128] The overhead and leveraged costs relate to marketing, corporate finance and accounting, human resources, legal, and amortization of acquisition-related intangibles and other costs that are not considered when management evaluates revenue generating segment performance, such as acquisition integration and severance costs.
[129] The business solutions in this segment include:
[130] Our global commercial services include solutions, both onshore and offshore, designed to meet the technology challenges facing clients, large or small, including financial institutions and non-financial institutions.
[131] These solutions range in scope from operations support for a single application to full management of information technology infrastructures.
[132] We also provide outsourcing teams to manage costs, improve operational efficiency and transform our clients' back-office and customer service processes.
[133] Our check authorization business provides check risk management and related services to businesses accepting or cashing checks.
[134] Our services assess the likelihood (and often provide a guarantee) that a check will clear.
[135] Our check authorization system uses artificial intelligence modeling and other state-of-the-art technology to deliver accuracy, convenience and simplicity to retailers.
[136] We completed the sale of our Public Sector and Education business to portfolio companies of Vista Equity Partners on February 1, 2017 (see Note 15 of the Notes to Consolidated Financial Statements).
[137] We have experienced sales personnel with expertise in particular services and markets, as well as in the needs of particular types of customers.
[138] We believe that focusing our expertise in specific markets (e.g., global financial institutions, North American financial institutions) and tailoring integrated solution sets of particular value to participants in those markets enables us to leverage opportunities to cross-sell and up-sell.
[139] We continue to realign our sales teams to better match our solution expertise with the market opportunity and customer demand.
[140] We target the majority of our potential customers via direct and/or indirect field sales, as well as inbound and outbound lead generation and telesales efforts.
[141] Our global marketing strategy is to develop and lead the execution of the IFS and GFS strategic marketing plans in support of their revenue and profitability goals and the FIS brand.
[142] Key components include thought leadership, integrated programs with consistent message development, internal and external communications, client conference content management, web content creation and management, trade shows, demand generation campaigns and collateral development and management.
[143] Patents, Copyrights, Trademarks and Other Intellectual Property
[144] The Company owns intellectual property, including trademarks, trade names, copyrights and patents, which we believe is important to our future success.
[145] Although we acquired the trademarks and trade names used by SunGard, we note that following the split-off of the Availability Services (“AS”) business by SunGard in 2014, AS has the right to use the Sungard Availability Services name, which does not include the right to use the SunGard name or its derivatives.
[146] We rely on a combination of contractual restrictions, internal security practices, patents, copyrights and applicable law to establish and protect our software, technology and expertise worldwide.
[147] We rely on trademark law to protect our rights in our brands.
[148] We intend to continue taking appropriate measures to protect our intellectual property rights, including by legal action when necessary and appropriate.
[149] In general, we own the proprietary rights necessary for the conduct of our business, although we do license certain items from third parties under arms-length agreements for varying terms, including some "open source" licenses.
[150] The markets for our solutions and services are intensely competitive.
[151] Depending on the business line, in both our IFS and GFS segments, our primary competitors include internal technology departments within financial institutions, retailers, data processing or software development departments of large companies or large computer manufacturers, companies that deliver software and integrated services to the financial services industry, third-party payment processors, securities exchanges, asset managers, card associations, clearing networks or associations, trust companies, independent computer services firms, companies that develop and deploy software applications, companies owned by global banks selling new competitive solutions, companies that provide customized development, implementation and support services, disruptive technology innovators, and business process outsourcing companies.
[152] Many of these companies compete with us across multiple solutions, markets and geographies.
[153] Some of these competitors possess greater financial, sales and marketing resources than we do.
[154] Competitive factors impacting the success of our services across our segments include the quality of the technology-based application or service, application features and functions, ease of delivery and integration, the ability to maintain, enhance and support the applications or services, price and overall relationship management.
[155] We believe we compete favorably in each of these categories.
[156] In addition, we believe our financial services industry expertise, combined with our ability to offer multiple applications, services and integrated solutions to individual clients, enhances our competitiveness against companies with more limited offerings.
[157] Our research and development activities have related primarily to the design and development of processing systems and related software applications and risk management platforms.
[158] We expect to continue our practice of investing an appropriate level of resources to maintain, enhance and extend the functionality of our proprietary systems and existing software applications, to develop new and innovative software applications and systems to address emerging technology trends in response to the needs of our clients and to enhance the capabilities of our outsourcing infrastructure.
[159] In addition, we intend to offer services compatible with new and emerging delivery channels.
[160] As part of our research and development process, we evaluate current and emerging technology for compatibility with our existing and future software platforms.
```

Gate response:

```text
[69]
```

#### Block 4: sentences 161–200

```text
[161] To this end, we engage with various hardware and software vendors in evaluation of various infrastructure components.
[162] Where appropriate, we use third-party technology components in the development of our software applications and service offerings.
[163] In the case of nearly all of our third-party software, enterprise license agreements exist for the third-party component and either alternative suppliers exist or transfer rights exist to ensure the continuity of supply.
[164] As a result, we are not materially dependent upon any third-party technology components.
[165] Third-party software may be used for highly specialized business functions, which we may not be able to develop internally within time and budget constraints.
[166] Additionally, third-party software may be used for commodity-type functions within a technology platform environment.
[167] We work with our clients to determine the appropriate timing and approach to introducing technology or infrastructure changes to our applications and services.
[168] During the years ended December 31, 2017 , 2016 and 2015 approximately 2% to 5% of revenues were non-capitalizable research and development expense.
[169] Our services are subject to a broad range of complex federal, state, and foreign regulation and requirements, as well as requirements under the rules of self-regulatory organizations, including federal truth-in-lending and truth-in-savings rules, Regulation AA (Unfair or Deceptive Acts or Practices), data protection and privacy laws, usury laws, laws governing state trust charters, the Equal Credit Opportunity Act, the Electronic Funds Transfer Act, the Fair Credit Reporting Act, the Fair Debt Collection Practices Act, the Bank Secrecy Act, the USA Patriot Act, the Internal Revenue Code, the Employee Retirement Income Security Act, the Health Insurance Portability and Accountability Act, the Community Reinvestment Act and the Dodd-Frank Wall Street Reform and Consumer Protection Act (the "Dodd-Frank Act"), the Securities Exchange Act of 1934 (the "1934 Act"), the Investment Advisors Act of 1940 (the "1940 Act"), the U.S. Foreign Corrupt Practices Act and UK Bribery Act, and the rules and regulations of the Financial Industry Regulatory Authority (“FINRA”), the Securities and Exchange Commission (“SEC”) and the Financial Conduct Authority in the U.K. (“FCA”).
[170] The compliance of our services and applications with these and other applicable laws and regulations depends on a variety of factors, including the manner in which our clients use them.
[171] In some cases, we are directly subject to regulatory oversight and examination.
[172] In other cases, our clients are contractually responsible for determining what is required of them under applicable laws and regulations so that we can assist them in their compliance efforts.
[173] In either case, the failure of our services to comply with applicable laws and regulations may result in restrictions on our ability to provide those services and/or the imposition of civil fines and/or criminal penalties.
[174] The principal areas of regulation impacting our business are:
[175] Oversight by Banking Regulators.
[176] As a provider of electronic data processing and back-office services to financial institutions, FIS is subject to regulatory oversight and examination by the Federal Banking Agencies ("FBA"), including the Federal Deposit Insurance Corporation ("FDIC"), the Office of the Comptroller of the Currency ("OCC"), the Board of Governors of the Federal Reserve System ("FRB"), the National Credit Union Administration ("NCUA") and the Consumer Financial Protection Bureau ("CFPB") as part of the Multi-Regional Data Processing Servicer Program ("MDPS").
[177] The MDPS program includes technology suppliers that provide mission critical applications for a large number of financial institutions that are regulated by multiple regulatory agencies.
[178] Periodic information technology examination assessments are performed using FBA Interagency guidelines to identify potential risks that could adversely affect serviced financial institutions, determine compliance with applicable laws and regulations that affect the services provided to financial institutions and ensure the services we provide to financial institutions do not create systemic risk to the banking system or impact the safe and sound operation of the financial institutions we process.
[179] In addition, independent auditors annually review several of our operations to provide reports on internal controls for our clients’ auditors and regulators.
[180] We are also subject to review and examination by state and international regulatory authorities under state and foreign laws and rules that regulate many of the same activities that are described above, including electronic data processing, payments and back-office services for financial institutions and the use of consumer information.
[181] Our U.S.-based wealth and retirement business holds charters in the states of Georgia and Delaware, which makes us subject to the regulatory compliance requirements of the Georgia Department of Banking and Finance and the State of
[182] Delaware Office of the State Bank Commissioner.
[183] As a result, we are also authorized to provide trust services in various additional states subject to additional applicable state regulations.
[184] Oversight by Securities Regulators.
[185] Our subsidiary that conducts our broker-dealer business in the U.S. is registered as a broker-dealer with the SEC, is a member of FINRA, and is registered as a broker-dealer in numerous states.
[186] Our broker-dealer is subject to regulation and oversight by the SEC.
[187] In addition, FINRA, a self-regulatory organization that is subject to oversight by the SEC, adopts and enforces rules governing the conduct, and examines the activities, of its member firms, including our broker-dealer.
[188] State securities regulators also have regulatory or oversight authority over our broker-dealer.
[189] Broker-dealers are subject to regulations that cover all aspects of the securities business, including sales methods, trade practices among broker-dealers, public and private securities offerings, use and safekeeping of customers’ funds and securities, capital structure, record keeping, the financing of customers’ purchases and the conduct and qualifications of directors, officers and employees.
[190] In particular, as a registered broker-dealer and member of a self-regulatory organization, we are subject to the SEC’s uniform net capital rule, Rule 15c3-1.
[191] Rule 15c3-1 specifies the minimum level of net capital a broker-dealer must maintain and also requires that a significant part of a broker-dealer’s assets be kept in relatively liquid form.
[192] The SEC and various self-regulatory organizations impose rules that require notification when net capital falls below certain predefined criteria, limit the ratio of subordinated debt to equity in the regulatory capital composition of a broker-dealer and constrain the ability of a broker-dealer to expand its business under certain circumstances.
[193] Additionally, the SEC’s uniform net capital rule imposes certain requirements that may have the effect of prohibiting a broker-dealer from distributing or withdrawing capital and requiring prior notice to the SEC for certain withdrawals of capital.
[194] Our subsidiaries also include an SEC-registered investment adviser and SEC-registered transfer agent.
[195] Our registered investment adviser is subject to the fiduciary and other obligations imposed on investment advisors under the 1940 Act, and the rules and regulations promulgated thereunder, as well as various state securities laws.
[196] Our registered transfer agent is subject to the 1934 Act and the rules and regulations promulgated thereunder.
[197] These laws and regulations generally grant the SEC and other supervisory bodies broad administrative powers to address non-compliance with regulatory requirements.
[198] Sanctions that may be imposed for non-compliance with these requirements include the suspension of individual employees, limitations on engaging in certain activities for specified periods of time or for specified types of clients, the revocation of registrations, other censures and significant fines.
[199] Subsidiaries engaged in activities outside the U.S. are regulated by various government agencies in the particular jurisdiction where they are chartered, incorporated and/or conduct their business activity.
[200] For example, pursuant to the U.K. Financial Services and Markets Act 2000 ("FSMA"), certain of our subsidiaries are subject to regulations promulgated and administered by the FCA.
```

Gate response:

```text
[61, 65, 68, 87, 89, 90]
```

Confirm response:

```text
[[169, 68, "T"]]
```

#### Block 5: sentences 201–240

```text
[201] The FSMA and rules promulgated thereunder govern all aspects of the U.K. investment business, including sales, research and trading practices, provision of investment advice, use and safekeeping of client funds and securities, regulatory capital, record keeping, margin practices and procedures, approval standards for individuals, anti-money laundering, periodic reporting and settlement procedures.
[202] The Company is subject to a number of privacy and data protection laws, regulations and directives globally (referred to collectively as “Privacy Laws”), many of which place restrictions on the Company’s ability to efficiently transfer, access and use personal data across its business.
[203] The legislative and regulatory landscape for privacy and data protection continues to evolve.
[204] Our financial institution clients operating in the United States are required to comply with privacy regulations imposed under the Gramm-Leach-Bliley Act (referred to as “GLBA”).
[205] GLBA places restrictions on the use of non-public personal information.
[206] All financial institutions must disclose detailed privacy policies to their customers and offer them the opportunity to direct the financial institution not to share information with third parties.
[207] The regulations under GLBA, however, permit financial institutions to share information with non-affiliated parties who perform services for the financial institutions.
[208] As a provider of services to financial institutions, we are required to comply with the privacy laws and are bound by the same limitations on disclosure of the information received from our clients as apply to the financial institutions themselves.
[209] A determination that there have been violations of privacy laws could expose us to significant damage awards, fines and other penalties that could, individually or in the aggregate, materially harm our business and reputation.
[210] In October 2015, the European Court of Justice ruled that the U.S.-EU Safe Harbor framework clauses, a compliance method by which we relied in portions of our business to transfer personal data regarding citizens of the EU to the U.S., could no longer be relied upon.
[211] The U.S. and EU authorities have agreed in principle on a replacement for Safe Harbor known as “Privacy Shield”.
[212] The Privacy Shield approach has not been fully endorsed by all relevant parties and there have already been challenges to this initiative in the European justice system.
[213] While we have certified certain lines of business under the Privacy Shield, we have chosen to adopt EU model clauses published by the European Commission as the primary basis for the export of data from the EU to the U.S.
[214] The EU has recently adopted a comprehensive overhaul of its data protection regime from the current national legislative approach to a single European Economic Area Privacy Regulation, the General Data Protection Regulation (“GDPR”), which comes into effect on May 26, 2018.
[215] The proposed EU data protection regime imposes a strict data compliance regime and extends the scope of the EU data protection law to all foreign companies processing data of EU residents.
[216] Although the GDPR will apply across the EU without a need for local implementing legislation, as has been the case under the current data protection regime, local data protection authorities (“DPAs”) will still have the ability to interpret the GDPR, which has the potential to create inconsistencies on a country-by-country basis.
[217] The Company has adopted a comprehensive global privacy program to assess and manage these evolving risks, including contract terms to comply with this new law.
[218] Elements of our cash access and money transmission businesses are registered as a Money Services Business and are subject to the USA Patriot Act and reporting requirements of the Bank Secrecy Act and U.S. Treasury Regulations.
[219] These businesses may also be subject to certain state, local and licensing requirements.
[220] The Financial Crimes Enforcement Network, state attorneys general, and other agencies have enforcement responsibility over laws relating to money laundering, currency transmission, and licensing.
[221] In applicable states, we have obtained money transmitter licenses.
[222] However, changes to state money transmission laws and regulations, including changing interpretations and the implementation of new or varying regulatory requirements, may result in the need for additional money transmitter licenses or for the requirement that we change the way in which we deliver certain services.
[223] We are also subject to certain economic and trade sanctions programs that are administered by the U.S. Treasury’s Office of Foreign Assets Control (referred to as “OFAC”), which prohibit or restrict transactions to or from or dealings with specified countries, their governments, and in certain circumstances, their nationals, and with individuals and entities that are specially-designated nationals of those countries, narcotics traffickers, and terrorists or terrorist organizations.
[224] Similar anti-money laundering laws apply to movements of currency and payments through electronic transactions and to dealings with persons specified in lists maintained by the country equivalents to OFAC in several other countries.
[225] We have implemented policies, procedures, and internal controls that are designed to comply with the regulations and economic sanctions programs administered by OFAC.
[226] Outside the U.S., applicable laws, rules and regulations similarly require designated types of financial institutions to implement anti-money laundering programs.
[227] We have implemented policies, procedures and internal controls that are designed to comply with all applicable anti-money laundering laws and regulations.
[228] Consumer Reporting and Protection.
[229] Our retail check authorization services (Certegy Check Services) and account opening services, including credit scoring analysis (ChexSystems), maintain databases of consumer information and, as a consequence, are subject to the Federal Fair Credit Reporting Act and similar state laws.
[230] Among other things, the Federal Fair Credit Reporting Act imposes requirements on us concerning data accuracy, and provides that consumers have the right to know the contents of their files, to dispute their accuracy, and to require verification or removal of disputed information.
[231] The Federal Trade Commission (FTC), as well as state attorneys general and other agencies, have enforcement responsibility over the collection laws, as well as the various credit reporting laws.
[232] In furtherance of our objectives of data accuracy, fair treatment of consumers, protection of consumers’ personal information, and compliance with these laws, we strive to, and have made considerable investment to, maintain a high level of security for our computer systems in which consumer data resides, and we maintain consumer relations call centers to facilitate efficient handling of consumer requests for information and handling disputes.
[233] We also are focused on ensuring our operating environments safeguard and protect consumer's personal information in compliance with these laws.
[234] Our consumer reporting and facing businesses are subject to CFPB bulletin 2013-7 (an update to the former Regulation A- Unfair Deceptive Acts or Practices), which states the definition of Unfair, Deceptive or Abusive Acts or Practices (UDAAP).
[235] This specific bulletin states that UDAAPs can cause significant financial injury to consumers, erode consumer confidence, and undermine fair competition in the financial marketplace.
[236] Original creditors and other covered persons and service providers under the Dodd-Frank Act involved in collecting debt related to any consumer financial product or service are subject to the prohibition against UDAAPs in the Dodd-Frank Act.
[237] Our collection services supporting our check, card and payment environments are subject to the Federal Fair Debt Collection Practices Act and various state collection laws and licensing requirements.
[238] Trade Commission, as well as state attorneys general and other agencies, have enforcement responsibility over the collection laws, as well as the various credit reporting laws.
[239] FIS is subject to applicable anti-corruption laws, such as the U.S. Foreign Corrupt Practices Act and the U.K. Bribery Act, in the jurisdictions in which it operates.
[240] Anti-corruption laws generally prohibit offering, promising, giving, or authorizing others to give anything of value, either directly or indirectly, to a government official or private party in order to influence official action or otherwise gain an unfair business advantage, such as to obtain or retain business.
```

Gate response:

```text
[65, 68]
```

Confirm response:

```text
[[202, 68, "T"], [203, 68, "T"], [204, 68, "T"], [205, 68, "T"], [206, 68, "T"], [207, 68, "T"], [208, 68, "T"], [209, 68, "T"], [210, 68, "T"], [211, 68, "T"], [212, 68, "T"], [213, 68, "T"], [214, 68, "T"], [215, 68, "T"], [216, 68, "T"], [217, 68, "O"], [228, 68, "N"], [229, 68, "T"], [230, 68, "T"], [231, 68, "T"], [232, 68, "O"], [233, 68, "O"], [234, 68, "T"], [235, 68, "T"], [236, 68, "T"], [237, 68, "T"], [238, 68, "T"]]
```

#### Block 6: sentences 241–259

```text
[241] FIS has implemented policies, procedures, and internal controls that are designed to comply with such laws, rules and regulations.
[242] The foregoing list of laws and regulations to which our Company is subject is not exhaustive, and the regulatory framework governing our operations changes continuously.
[243] Enactment of new laws and regulations may increasingly affect the operations of our business, directly and indirectly, which could result in substantial regulatory compliance costs, litigation expense, adverse publicity, and/or loss of revenue.
[244] Globally, attacks on information technology systems continue to grow in frequency, complexity and sophistication.
[245] Such attacks have become a point of focus for individuals, businesses and governmental entities.
[246] The objectives of these attacks include, among other things, gaining unauthorized access to systems to facilitate financial fraud, disrupt operations, cause denial of service events, corrupt data, and steal non-public, sensitive information.
[247] As part of our business, we electronically receive, process, store and transmit a wide range of confidential information, including sensitive customer information and personal consumer data.
[248] We also operate payment, cash access and prepaid card systems.
[249] FIS remains focused on making strategic investments in information security to protect our clients and our information systems.
[250] This includes both capital expenditures and operating expenses on hardware, software, personnel and consulting services.
[251] We also participate in industry and governmental initiatives to improve information security for our clients.
[252] For more information on Information Security, see "Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations ."
[253] As of December 31, 2017 , we had more than 53,000 employees, including approximately 34,000 employees principally employed outside of the U.S. None of our U.S. workforce currently is unionized.
[254] Approximately 12,000 of our employees, primarily in Brazil, Germany, Tunisia, France, Italy, and Chile, are represented by labor unions or works councils.
[255] Our internet website address is www.fisglobal.com.
[256] We make our Annual Reports on Form 10-K, Quarterly Reports on Form 10-Q, and Current Reports on Form 8-K, and any amendments to those reports, available, free of charge, on that website as soon as reasonably practicable after we file or furnish them to the Securities and Exchange Commission.
[257] Our Corporate Governance Policy and Code of Business Conduct and Ethics are also available on our website and are available in print, free of charge, to any shareholder who mails a request to the Corporate Secretary, Fidelity National Information Services, Inc., 601 Riverside Avenue, Jacksonville, FL 32204 USA.
[258] Other corporate governance-related documents can be found at our website as well.
[259] However, the information found on our website is not a part of this or any other report.
```

Gate response:

```text
[61, 65, 68]
```

Confirm response:

```text
[]
```
