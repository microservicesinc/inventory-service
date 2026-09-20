# 🚀 AWS CDK V2 Masterclass Study Guide & Progress Checklist (Python Edition)

## 🟩 Section 1: Core Framework Architecture & Setup
- [ ] **Course Introduction (3:16)**
  * *Docs:* [AWS CDK Home Overview]
  * *Video Guide:* [AWS CDK Crash Course (FreeCodeCamp)]
- [ ] **Introduction to AWS CDK (6:29)**
  * *Docs:* [CDK Core Concepts & CloudFormation]
  * *Video Guide:* [AWS CDK vs SDK Structural Comparison]
- [ ] **Initializing Your CDK Environment & Bootstrapping (15:23)**
  * *Docs:* [CDK Prerequisites & Bootstrap Setup]
  * *Video Guide:* [Python CDK Project Environment Setup]
- [ ] **Creating Your First CDK App (15:23)**
  * *Docs:* [Tutorial: Build & Deploy Your First App]
  * *Video Guide:* [CDK App Architecture Breakdown]
- [ ] **CDK App Lifecycle & Synthesizing Cloud Assemblies (11:12)**
  * *Docs:* [The App Lifecycle Phases Explained]
  * *Video Guide:* [CDK App Lifecycle Workflow Breakdown]
- [ ] **Deploying Your CDK Stack to AWS (10:08)**
  * *Docs:* [Deploying CDK Applications]
  * *Video Guide:* [CLI Commands Deep Dive (`synth`, `deploy`)]
- [ ] **Destroying Your CDK Stack Cleanly (6:29)**
  * *Docs:* [Demolishing CDK Stacks]
  * *Video Guide:* [CLI Commands Deep Dive (`synth`, `deploy`)]

## 🟦 Section 2: Building Blocks (Construct Anatomy)
- [ ] **Section 2 Introduction (2:51)**
- [ ] **Creating an Empty CDK App (7:42)**
  * *Docs:* [Understanding CDK Project Structures]
  * *Video Guide:* [CDK Directory & `cdk.json` Walkthrough]
- [ ] **L1 Constructs & The Underlying CloudFormation Library (17:35)**
  * *Docs:* [Construct Levels: L1, L2, and L3 Patterns]
  * *Video Guide:* [Difference Between L1 vs L2 Constructs]
- [ ] **Updating and Mutating Your Deployed CDK App (13:28)**
- [ ] **Introduction to Smart L2 Constructs (13:47)**
  * *Docs:* [Best practices for AWS CDK constructs]
  * *Video Guide:* [Building Custom Infrastructure with L2 Modules]
- [ ] **Configuring L2 Construct Properties & Default Settings (13:30)**
- [ ] **Adding Related Infrastructure via Instance Methods (12:38)**
- [ ] **Granting IAM Permissions on L2 Constructs Effortlessly (5:27)**
  * *Docs:* [Granting IAM Permissions via Short Methods]
  * *Video Guide:* [IAM Roles & Policies using `grant_read_write()`]
- [ ] **Configuring Stack Outputs (`CfnOutput`) on CDK (5:32)**
  * *Docs:* [Defining CloudFormation Outputs in CDK]
  * *Video Guide:* [Stack Parameters, Outputs, and CloudWatch Alarms]
- [ ] **Harnessing the Built-in Metrics of L2 Constructs (13:25)**
- [ ] **Introduction to CDK Patterns & Architectural Templates (L3) (12:35)**
  * *Docs:* [Using AWS Solutions Construct Patterns]
  * *Video Guide:* [Deploying High-Level L3 Patterns Fast]
- [ ] **Implementing Complete Solutions via CDK Patterns (10:47)**

## 🟨 Section 3: Network Topologies & Assets
- [ ] **Section 3 Introduction (2:01)**
- [ ] **Allowing Network Connections & Security Rules on AWS CDK (15:29)**
  * *Docs:* [Managing Security Groups via Security APIs]
  * *Video Guide:* [VPC Configurations, Subnets, and Peer Routing]
- [ ] **Allowing Connections and Traffic to a Default Port (12:41)**
- [ ] **Safely Removing Resources and Deletion Policies (3:25)**
  * *Docs:* [Resource Removal Policies (`RemovalPolicy`)]
  * *Video Guide:* [Configuring `RemovalPolicy.DESTROY` vs `RETAIN`]
- [ ] **Uploading Local Files & Images with S3 Assets on AWS CDK (13:09)**
  * *Docs:* [Deploying Files and Docker Images as Assets]
  * *Video Guide:* [Bundling Lambda Functions & Frontend Code]

## 🟪 Section 4: Enterprise Design & Multi-Stack Layouts
- [ ] **Section 4 Introduction (1:25)**
- [ ] **Setting up Cross-stack References with AWS CDK (15:47)**
  * *Docs:* [Passing Outputs Between Stacks]
  * *Video Guide:* [Cross-Stack References & Export Dependency Errors]
- [ ] **Splitting Infrastructure via Nested Stacks with AWS CDK (14:13)**
  * *Docs:* [Working with `NestedStack` Architecture]
  * *Video Guide:* [When to Use Nested Stacks vs Split Stacks]

## 🟥 Section 5: Enforcement, Compliance, & Automated Unit Tests
- [ ] **Section 5 Introduction (1:57)**
- [ ] **Tagging Your CDK Constructs for Cost Allocation (13:12)**
  * *Docs:* [Applying AWS Resource Tags via `Tags.of()`]
  * *Video Guide:* [Global Resource Tagging Strategies]
- [ ] **Introduction to CDK Aspects Visitor Patterns (11:20)**
  * *Docs:* [Applying the Visitor Pattern via CDK Aspects]
  * *Video Guide:* [Building Customs Policies with CDK Aspects]
- [ ] **Resource Validation with CDK Aspects (9:36)**
- [ ] **Programmatically Modifying Resources via CDK Aspects (5:13)**
- [ ] **Resolving Non-Literal Values and CDK Tokens in Aspects (11:53)**
- [ ] **Introduction to Unit Testing Your CDK Stacks (11:34)**
  * *Docs:* [Testing Framework for AWS CDK Assertions]
  * *Video Guide:* [Unit Testing Stacks via Pytest]
- [ ] **Testing Construct Properties with Fine-grained Assertions (10:08)**
- [ ] **Crafting Complex Assertions with Array & Object Matchers (8:26)**

## 🏁 Wrap-up
- [ ] **Course Conclusion & Key Infrastructure Milestones (1:10)**
- [ ] **Bonus Lecture: Join My Other Courses! (1:49)**
