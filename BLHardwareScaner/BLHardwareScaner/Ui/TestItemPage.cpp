
#include "TestItemPage.h"

#include <QtCore/QFile>

#include "TestItem\\DiskSpeedPage.h"

#define STRING_TESTITEM_DISK_SPEED QObject::tr("Disk Speed")

TestItemPage::TestItemPage(QWidget *parent, Qt::WFlags flags)
    : QWidget(parent, flags)
{
    ui.setupUi(this);
    this->LoadQSS();

    m_bInitDone = false;
    m_uiRatio = 1.0f;

    m_pDiskSpeedPage = new DiskSpeedPage();
}

TestItemPage::~TestItemPage()
{
    if (m_pDiskSpeedPage != 0)
    {
        delete m_pDiskSpeedPage;
        m_pDiskSpeedPage = 0;
    }
}

void TestItemPage::SetUIRatio(IN float ratio)
{
    m_uiRatio = ratio;
}


void TestItemPage::showEvent(QShowEvent* e)
{
    if (!m_bInitDone)
    {
        this->Init();
        m_bInitDone = true;
    }
}

void TestItemPage::Init()
{
    connect(ui.listWidgetTestItem, SIGNAL(itemClicked(QListWidgetItem*)), this, SLOT(TestItemDoubleClicked(QListWidgetItem*)));
    // 设置属性
    ui.listWidgetTestItem->setViewMode(QListView::IconMode);
    ui.listWidgetTestItem->setIconSize(QSize(64 * m_uiRatio, 64 * m_uiRatio));
    ui.listWidgetTestItem->setMovement(QListView::Static);
    ui.listWidgetTestItem->setResizeMode(QListView::Adjust);

    this->AddTestItem(STRING_TESTITEM_DISK_SPEED, QIcon(".\\Image\\TestItem\\DiskSpeed.png"));

    ui.stackedWidget->addWidget(m_pDiskSpeedPage);
    ui.stackedWidget->setCurrentWidget(m_pDiskSpeedPage);
}

void TestItemPage::AddTestItem(IN const QString& name, IN const QIcon& icon)
{
    // 虽然使用new方法, 但是pItem已设置父对象, 所以可以不delete
    // Qt机制: 父对象被析构时, 自动析构子对象
    QListWidgetItem* pItem = new QListWidgetItem(ui.listWidgetTestItem);
    pItem->setIcon(icon);
    pItem->setText(name);
    pItem->setTextAlignment(Qt::AlignHCenter);
    pItem->setFlags(Qt::ItemIsSelectable | Qt::ItemIsEnabled);
}

void TestItemPage::LoadQSS()
{
    QFile qssFile(".\\Qss\\Default\\TestItemPage.qss");  
    qssFile.open(QFile::ReadOnly);  

    if(qssFile.isOpen())  
    {  
        QString qss = qssFile.readAll();
        qssFile.close();  

        this->setStyleSheet(qss);
    } 
}

void TestItemPage::TestItemClicked(QListWidgetItem* pItem)
{
    if (NULL == pItem)
        return;

    if (pItem->text() == STRING_TESTITEM_DISK_SPEED)
    {
        ui.stackedWidget->setCurrentWidget(m_pDiskSpeedPage);
    }
}