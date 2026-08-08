# Title
Configuring Auto-Scaling for Contoso Web Apps
# Summary
This article describes how to configure auto-scaling for Contoso Web Apps that run on the Fabrikam Cloud Platform. It is intended for cloud administrators who manage production web workloads.

# Prerequisites
Before you start, make sure that:
* You have a Fabrikam Cloud subscription.
* You have at least one Contoso Web App deployed in a region.
* Your account has permission to create and edit scaling policies.
# Terminology
* **Auto-scaling:** A cloud feature that automatically adds or removes compute instances based on demand.
* **Scaling policy:** A rule set that defines when and how the platform scales resources.
* **Instance:** A running virtual machine or container that hosts the web app.

# Limitations
Auto-scaling does not support classic Contoso Web Apps. Migrate classic apps to the current Contoso Web App model before you enable auto-scaling.
# Configure auto-scaling
## Step 1: Open the Auto-Scaling page
1. Sign in to the Fabrikam Cloud portal.
2. On the left navigation pane, select Web Apps.
3. Select the Contoso Web App that you want to configure.
4. On the Overview page, select Auto-Scaling.

Step 2: Create a scaling policy
1. On the ** Auto-Scaling** page, select** Add policy**.
2. In the **Policy name** box, enter a short descriptive name, such as **Production weekday traffic**.
3. In the **Policy scope** list, select **Web app instances**.
4. In the **Minimum instances** box, enter **2**.
5. In the **Maximum instances** box, enter **10**.
6. In the **Default instances** box, enter **3**.

## Step 3: Define scale-out conditions
1. In the **Conditions** section, select **Add condition**.
2. In the **Metric** list, select **CPU percentage**.
3. In the **Operator** list, select **Greater than**.
4. In the **Threshold** box, enter **70**.
5. In the **Duration** list, select **10 minutes**.
6. In the **Action** list, select **Increase instances**.
7. In the **Change by** box, enter **2**.

## Step 4: Define scale-in conditions
1. In the **Conditions** section, select **Add condition**.
2. In the **Metric** list, select **CPU percentage**.
3. In the **Operator** list, select **Less than**.
4. In the **Threshold** box, enter **40**.
5. In the **Duration** list, select **15 minutes**.
6. In the **Action** list, select **Decrease instances**.
7. In the **Change by** box, enter **1**.

## Step 5: Save and enable the policy
1. Review the policy settings to confirm that the minimum, maximum, and default values match your requirements.
2. Select **Save**. 
3. On the Auto-Scaling page, turn on Enable auto-scaling.

# Verify auto-scaling behavior
1. To verify that auto-scaling works as expected, generate test load for the Contoso Web App.
2. Use your standard load test tool to gradually increase traffic for at least 30 minutes.
3. In the Fabrikam Cloud portal, monitor the Instances chart.
4. Confirm that the number of instances increases when CPU usage stays above the threshold for the configured duration. 
5. After the test load ends, confirm that the number of instances decreases when CPU usage stays below the scale‑in threshold.

#Troubleshooting
If auto-scaling does not behave as expected, review the following items.
1. Confirm that the scaling policy is enabled.
2. Check for overlapping policies that target the same web app.
Check for overlapping policies that target the same web app.
3. Verify that performance metrics are available for the web app.
4. Review recent activity logs for errors related to scaling operations.

# Security considerations
Auto-scaling uses the same identity and access controls as other Fabrikam Cloud resources. Limit policy creation and modification to administrators.

# Change history
* **Version 1.0:** Initial publication.
* **Version 1.1:** Updated scale‑in threshold and added security considerations.
