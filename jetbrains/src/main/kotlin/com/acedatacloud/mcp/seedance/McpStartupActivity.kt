package com.acedatacloud.mcp.seedance

import com.intellij.notification.NotificationGroupManager
import com.intellij.notification.NotificationType
import com.intellij.openapi.actionSystem.AnAction
import com.intellij.openapi.actionSystem.AnActionEvent
import com.intellij.openapi.options.ShowSettingsUtil
import com.intellij.openapi.project.Project
import com.intellij.openapi.startup.ProjectActivity

class McpStartupActivity : ProjectActivity {

    override suspend fun execute(project: Project) {
        val settings = McpSettings.getInstance()
        if (settings.state.hasShownSetupNotification) return

        settings.state.hasShownSetupNotification = true

        val notification = NotificationGroupManager.getInstance()
            .getNotificationGroup("Seedance MCP")
            .createNotification(
                "Seedance MCP",
                "Configure your API token and set up AI Assistant MCP integration.",
                NotificationType.INFORMATION,
            )

        notification.addAction(object : AnAction("Open Settings") {
            override fun actionPerformed(e: AnActionEvent) {
                ShowSettingsUtil.getInstance()
                    .showSettingsDialog(project, McpSettingsConfigurable::class.java)
                notification.expire()
            }
        })

        notification.notify(project)
    }
}
